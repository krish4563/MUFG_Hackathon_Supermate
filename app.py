import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from utils import load_user_transactions, load_prices_csv
from agents import BehaviorAgent, FraudAgent, PortfolioAgent
from arbiter import merge_agent_outputs
from rag import rag_answer, add_documents, init_indexer

load_dotenv()

st.set_page_config(page_title="Agentic RAG Prototype", layout="wide")
st.title("Agentic RAG — Prototype")

# --- Onboarding Step (collect user info once) ---
if "user_profile" not in st.session_state:
    with st.form("onboarding_form"):
        st.subheader("Tell us about yourself before we start")
        age = st.number_input("Your age", 18, 100, 30)
        goal = st.text_input("Your main financial goal (e.g., retire early, buy house, etc.)")
        risk = st.selectbox("Risk preference", ["Low", "Moderate", "High"])
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state["user_profile"] = {
                "age": age,
                "goal": goal,
                "risk": risk
            }
            st.success("Profile saved! Scroll down to start chatting.")
else:
    st.sidebar.write("✅ Profile loaded")
    st.sidebar.json(st.session_state["user_profile"])

# Sidebar: user info
st.sidebar.header("User Profile")
user_id = st.sidebar.text_input("User ID", value="user_1")
initial_capital = st.sidebar.number_input("Initial capital (₹)", value=100000.0, step=1000.0)
years = st.sidebar.slider("Projection years", 5, 40, 20)

# Uploads
st.sidebar.header("Upload data")
txn_file = st.sidebar.file_uploader("Upload transactions dataset (Excel/CSV)", type=["csv", "xlsx"])
prices_file = st.sidebar.file_uploader("Upload price history CSV (date,close)", type=["csv"])

# Chat section
st.header("Chat with your financial agent")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

query = st.text_input("Enter your question")

col1, col2 = st.columns(2)

# Load data
df_txn, prices_df = None, None
if txn_file:
    df_txn = load_user_transactions(txn_file)
    st.sidebar.success(f"Loaded transactions: {len(df_txn)} rows")

if prices_file:
    prices_df = load_prices_csv(prices_file)
    st.sidebar.success(f"Loaded prices: {len(prices_df)} rows")

# Initialize indexer once
if "indexer_init" not in st.session_state:
    init_indexer()
    st.session_state["indexer_init"] = True

# Preview
with col1:
    st.subheader("Transactions preview")
    if df_txn is not None:
        st.dataframe(df_txn.head(10))
    else:
        st.info("Upload transactions to enable Behavior & Fraud agents.")

with col2:
    st.subheader("Price data preview")
    if prices_df is not None:
        st.dataframe(prices_df.head(10))
    else:
        st.info("Upload prices CSV to enable Portfolio agent.")

# Run agents + chat
if st.button("Ask / Run agents"):
    # Behavior agent
    behavior_agent = BehaviorAgent(df_txn)
    behavior_agent.fit()
    behavior_profile = behavior_agent.profile_user(user_id)

    # Fraud agent
    fraud_agent = FraudAgent(df_txn)
    fraud_out = fraud_agent.detect_user_anomalies(user_id)

    # Portfolio agent
    portfolio_agent = PortfolioAgent(prices_df)
    portfolio_out = portfolio_agent.run_simulation(
        initial_capital=initial_capital, years=years, n_sim=500
    ) or {}

    # Arbiter merge
    combined = merge_agent_outputs(behavior_profile, fraud_out, portfolio_out)

    # Add user query to memory
    st.session_state['chat_history'].append({"role": "user", "content": query})

    # Trim to last 10 messages (5 Q/A pairs)
    st.session_state["chat_history"] = st.session_state["chat_history"][-10:]

    # Add docs for RAG
    docs = [msg["content"] for msg in st.session_state["chat_history"]]
    metadatas = [{"role": msg["role"]} for msg in st.session_state["chat_history"]]
    add_documents(docs, metadatas)

    # Generate RAG-based personalized LLM answer
    rag_resp = rag_answer(
        query if query else "Provide financial plan summary for this user.",
        user_id,
        behavior_profile,
        fraud_out,
        portfolio_out,
        combined,
        user_profile=st.session_state.get("user_profile", {})
    )

    # Add assistant response to memory
    st.session_state['chat_history'].append({"role": "assistant", "content": rag_resp})

# --- Show Chat History like GPT ---
st.subheader("Conversation")
for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
