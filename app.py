import streamlit as st
import os
from rag import rag_answer

# Page config
st.set_page_config(page_title="SuperMate - AI Retirement Advisor", layout="wide")

# Initialize session state
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------- Onboarding ---------------- #
if st.session_state["user_profile"] is None:
    st.title("👋 Welcome to SuperMate")
    st.subheader("Your AI Investment Advisor for Retirement Planning")

    with st.form("onboarding_form"):
        st.markdown("### Tell us about yourself")

        age = st.number_input("Your current age", 18, 70, 30)
        retirement_age = st.number_input("Planned retirement age", 40, 75, 60)
        super_balance = st.number_input("Current superannuation balance (₹)", min_value=0.0, value=500000.0, step=5000.0)
        monthly_contribution = st.number_input("Planned monthly contribution (₹)", min_value=0.0, value=20000.0, step=500.0)
        risk = st.selectbox("Risk preference", ["Low", "Moderate", "High"])
        goal = st.text_input("Retirement goal (short)")
        desired_annual_income = st.number_input("Desired annual retirement income (₹)", min_value=0.0, value=0.0, step=1000.0)

        # 🔥 New metadata
        monthly_expenses = st.number_input("Current monthly expenses (₹)", min_value=0.0, value=30000.0, step=1000.0)
        debt_level = st.number_input("Outstanding debt (₹)", min_value=0.0, value=0.0, step=10000.0)
        dependents = st.number_input("Number of dependents", min_value=0, value=0, step=1)

        st.markdown("### Upload your financial data (optional)")
        txn_file = st.file_uploader("Transactions (CSV / XLSX)", type=["csv", "xlsx"])
        prices_file = st.file_uploader("Price history CSV (date,close)", type=["csv"])

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
                "monthly_expenses": float(monthly_expenses),
                "debt_level": float(debt_level),
                "dependents": int(dependents),
                "txn_file": txn_file,
                "prices_file": prices_file,
            }
            st.rerun()

# ---------------- Chatbot ---------------- #
else:
    st.title("💬 SuperMate Chat")
    st.markdown("Ask me anything about your retirement plan.")

    # Sidebar for history
    with st.sidebar:
        st.header("Chat History")
        for i, msg in enumerate(st.session_state["messages"]):
            if msg["role"] == "user":
                st.text(f"Q{i+1}: {msg['content'][:30]}...")

        if st.button("Reset conversation"):
            st.session_state["messages"] = []
            st.rerun()

    # Chat display
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # Input box
    if query := st.chat_input("Type your question here..."):
        st.session_state["messages"].append({"role": "user", "content": query})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = rag_answer(
                    query=query,
                    user_profile=st.session_state["user_profile"],
                    txn_file=st.session_state["user_profile"].get("txn_file"),
                    prices_file=st.session_state["user_profile"].get("prices_file"),
                )
                st.markdown(answer)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
