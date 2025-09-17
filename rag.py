import os
from indexer import get_indexer
from dotenv import load_dotenv

load_dotenv()

INDEXER = None

def init_indexer():
    global INDEXER
    INDEXER = get_indexer()

def add_documents(texts, metadatas):
    global INDEXER
    if INDEXER is None:
        init_indexer()
    if hasattr(INDEXER, "build"):
        INDEXER.build(texts, metadatas)
    else:
        INDEXER.upsert(texts, metadatas)

def retrieve(query, top_k=5):
    global INDEXER
    if INDEXER is None:
        init_indexer()
    return INDEXER.query(query, top_k=top_k)

# LLM wrapper (Gemini)
def call_gemini(prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return resp.text

def _format_portfolio_text(portfolio_out: dict) -> str:
    if not portfolio_out:
        return "No portfolio simulation available."
    lines = []
    for strat, v in portfolio_out.items():
        s = v.get("sim_summary", {})
        lines.append(f"{strat}: median={s.get('median'):.0f}, p10={s.get('p10'):.0f}, p90={s.get('p90'):.0f}")
    return "\n".join(lines)

def rag_answer(query: str, user_id: str, behavior, fraud, portfolio, arbiter, user_profile=None) -> str:
    docs = retrieve(query, top_k=5)
    context_text = "\n\n".join([d.get("text", str(d)) for d in docs])

    profile_text = ""
    if user_profile:
        profile_text = (f"Age: {user_profile.get('age')}, Retirement age: {user_profile.get('retirement_age')}, "
                        f"Current super: ₹{user_profile.get('super_balance'):.0f}, Monthly contribution: ₹{user_profile.get('monthly_contribution'):.0f}, "
                        f"Risk: {user_profile.get('risk')}, Goal: {user_profile.get('goal')}, Desired annual income: ₹{user_profile.get('desired_annual_income',0):.0f}")

    portfolio_text = _format_portfolio_text(portfolio)

    agent_context = f"""
User ID: {user_id}
{profile_text}

Behavior profile: {behavior}
Fraud detection: {fraud}
Portfolio simulation (per strategy):
{portfolio_text}

Arbiter decision: {arbiter}
    """

    prompt = f"""
You are an expert retirement planning assistant tailored for superannuation users.

Prior relevant chat / documents (retrieved):
{context_text}

Structured data:
{agent_context}

User asked:
{query}

Task:
- Use the structured data and retrieved context to provide a personalized, concise, and actionable response.
- Refer explicitly to the user's profile, portfolio strategy outcomes, fraud/behavior flags, and the arbiter decision.
- If the portfolio simulations show risk, provide specific next steps (e.g., increase contribution, shift allocation, consult CFP).
- Keep language simple and numerical references clear (use rupee amounts rounded).

Answer:
"""
    answer = call_gemini(prompt)
    return answer
