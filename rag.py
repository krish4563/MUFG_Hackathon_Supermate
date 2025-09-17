import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please check your .env file.")
genai.configure(api_key=api_key)

def rag_answer(query, user_profile=None, txn_file=None, prices_file=None):
    """
    Build context from user profile + documents and send query to Gemini
    """

    # ✅ Build profile context
    profile_text = ""
    if user_profile:
        profile_text = (
            f"Age: {user_profile.get('age')}, Retirement age: {user_profile.get('retirement_age')}, "
            f"Current super: ₹{user_profile.get('super_balance'):.0f}, "
            f"Monthly contribution: ₹{user_profile.get('monthly_contribution'):.0f}, "
            f"Risk: {user_profile.get('risk')}, Goal: {user_profile.get('goal')}, "
            f"Desired annual income: ₹{user_profile.get('desired_annual_income',0):.0f}, "
            f"Monthly expenses: ₹{user_profile.get('monthly_expenses',0):.0f}, "
            f"Debt: ₹{user_profile.get('debt_level',0):.0f}, "
            f"Dependents: {user_profile.get('dependents',0)}"
        )

    # ✅ Transaction data context
    txn_text = ""
    if txn_file:
        try:
            if txn_file.name.endswith(".csv"):
                df = pd.read_csv(txn_file)
            else:
                df = pd.read_excel(txn_file)
            txn_text = f"Uploaded {len(df)} transactions with columns {list(df.columns)}"
        except Exception as e:
            txn_text = f"Error reading transactions: {e}"

    # ✅ Price history context
    price_text = ""
    if prices_file:
        try:
            df = pd.read_csv(prices_file)
            price_text = f"Uploaded price history with {len(df)} rows, columns: {list(df.columns)}"
        except Exception as e:
            price_text = f"Error reading price file: {e}"

    # Combine into context
    context = f"""
    USER PROFILE:
    {profile_text}

    TRANSACTIONS:
    {txn_text}

    PRICE HISTORY:
    {price_text}

    QUESTION:
    {query}
    """

    # Call Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(context)

    return response.text if hasattr(response, "text") else str(response)
