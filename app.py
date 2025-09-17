import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from utils import load_user_transactions, load_prices_csv
from agents import BehaviorAgent, FraudAgent, PortfolioAgent
from arbiter import merge_agent_outputs
from rag import rag_answer, add_documents, init_indexer

load_dotenv()

st.set_page_config(page_title="AI Superannuation Advisor", layout="wide")
st.title("AI Investment Advisor — Superannuation")

# --- Onboarding Step (Retirement / Superannuation focus) ---
if "user_profile" not in st.session_state:
    with st.form("onboarding_form"):
        st.subheader("Tell us about your retirement plan")
        age = st.number_input("Your current age", 18, 70, 30)
        retirement_age = st.number_input("Planned retirement age", 40, 75, 60)
        super_balance = st.number_input("Current superannuation balance (₹)", min_value=0.0, value=500000.0, step=5000.0)
        monthly_contribution = st.number_input("Planned monthly contribution (₹)", min_value=0.0, value=20000.0, step=500.0)
        risk = st.selectbox("Risk preference", ["Low", "Moderate", "High"])
        goal = st.text_input("Retirement goal (short): e.g., 'Comfortable living' / 'Travel' / 'Healthcare security'")
        desired_annual_income = st.number_input("Desired annual retirement income (₹) — optional", min_value=0.0, value=0.0, step=1000.0)

        # uploads on onboarding page
        st.markdown("### Upload your financial data (recommended)")
        txn_file = st.file_uploader("Transactions (CSV / XLSX) — optional", type=["csv", "xlsx"])
        prices_file = st.file_uploader("Price history CSV (date,close) — optional", type=["csv"])

        submitted = st.form_submit_button("Save profile & continue")
        if submitted:
            st.session_state["user_profile"] = {
                "age": int(age),
                "retirement_age": int(retirement_age),
                "super_balance": float(super_balance),
                "monthly_contribution": float(monthly_contribution),
                "risk": risk,
                "goal": goal,
                "desired_annual_income": float(desired_annual_income),
                "txn_file": txn_file,
                "prices_file": prices_file,
            }
            st.success("Profile saved! Scroll down to start chatting.")

if "user_profile" in st.session_state:
    st.sidebar.header("Your retirement profile")
    st.sidebar.json({k: v for k, v in st.session_state["user_profile"].items() if k not in ("txn_file", "prices_file")})

# Chat region
st.header("Chat with your Superannuation Advisor")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # list of {"role":"user"/"assistant", "content": str}

# initialize indexer
if "indexer_init" not in st.session_state:
    init_indexer()
    st.session_state["indexer_init"] = True

# load uploaded files (from onboarding stored in session)
df_txn = None
prices_df = None
if "user_profile" in st.session_state:
    prof = st.session_state["user_profile"]
    if prof.get("txn_file") is not None:
        df_txn = load_user_transactions(prof["txn_file"])
    if prof.get("prices_file") is not None:
        prices_df = load_prices_csv(prof["prices_file"])

# Chat input
query = st.chat_input("Ask about your superannuation plan (e.g., 'Am I on track to retire at 60?')")

# Show history on left, chat box on right
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("Recent conversation")
    for msg in st.session_state["chat_history"][-10:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Advisor:** {msg['content']}")

with right_col:
    st.subheader("Conversation")

    if query:
        # append user message
        st.session_state["chat_history"].append({"role": "user", "content": query})
        st.session_state["chat_history"] = st.session_state["chat_history"][-10:]

        # Run agents
        behavior_profile = {"behavior_cluster": None}
        fraud_out = {"anomaly_score": 0, "alerts": []}
        portfolio_out = {}

        # pick user_id
        user_id = "user_1"
        if df_txn is not None:
            uids = df_txn["user_id"].unique()
            if len(uids) == 1:
                user_id = uids[0]

            behavior_agent = BehaviorAgent(df_txn)
            behavior_agent.fit()
            behavior_profile = behavior_agent.profile_user(user_id)

            fraud_agent = FraudAgent(df_txn)
            fraud_out = fraud_agent.detect_user_anomalies(user_id)

        # Portfolio
        profile = st.session_state.get("user_profile", {})
        years_left = max(1, profile.get("retirement_age", 65) - profile.get("age", 30))

        portfolio_agent = PortfolioAgent(prices_df)
        portfolio_out = portfolio_agent.run_superannuation_simulation(
            initial_balance=profile.get("super_balance", 0.0),
            monthly_contribution=profile.get("monthly_contribution", 0.0),
            years=years_left,
            n_sim=1000,
        )

        # Arbiter
        combined = merge_agent_outputs(behavior_profile, fraud_out, portfolio_out)

        # Add docs for RAG
        docs = [m["content"] for m in st.session_state["chat_history"]]
        metadatas = [{"role": m["role"]} for m in st.session_state["chat_history"]]
        add_documents(docs, metadatas)

        # RAG answer
        rag_resp = rag_answer(
            query,
            user_id,
            behavior_profile,
            fraud_out,
            portfolio_out,
            combined,
            user_profile=profile,
        )

        st.session_state["chat_history"].append({"role": "assistant", "content": rag_resp})
        st.session_state["chat_history"] = st.session_state["chat_history"][-10:]
        st.rerun()

# show conversation (bottom)
st.write("---")
st.subheader("Full remembered chat (last 5 Q/A pairs)")
for msg in st.session_state["chat_history"][-10:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Advisor:** {msg['content']}")
