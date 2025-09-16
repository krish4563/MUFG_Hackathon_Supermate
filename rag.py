import os
from indexer import get_indexer
from dotenv import load_dotenv

load_dotenv()

INDEXER = None

def init_indexer():
    global INDEXER
    INDEXER = get_indexer()

def add_documents(texts, metadatas):
    idx = get_indexer()
    if hasattr(idx, "build"):
        idx.build(texts, metadatas)
    else:
        idx.upsert(texts, metadatas)

def retrieve(query, top_k=5):
    if INDEXER is None:
        init_indexer()
    return INDEXER.query(query, top_k=top_k)

# === LLM wrapper ===
def call_gemini(prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return resp.text

def rag_answer(query: str, user_id: str, behavior, fraud, portfolio, arbiter, user_profile=None) -> str:
    """
    Personalized RAG answer that uses:
    - Retrieved documents
    - User profile + agent outputs
    - User query
    """
    docs = retrieve(query, top_k=5)
    context_text = "\n\n".join([d.get("text", str(d)) for d in docs])

    profile_text = f"User profile: {user_profile}" if user_profile else "No extra profile provided."

    agent_context = f"""
User ID: {user_id}
{profile_text}
Behavior profile: {behavior}
Fraud detection: {fraud}
Portfolio simulation: {portfolio}
Arbiter decision: {arbiter}
    """

    prompt = f"""
You are a financial advisor AI.

Here is prior chat context (last 5 turns):
{context_text}

Here is structured data from agents and onboarding profile:
{agent_context}

User query:
{query}

Now generate a personalized, easy-to-understand explanation/plan for the user. 
- Be conversational (chat style).
- Be concise but insightful.
- Highlight risks, behaviors, and portfolio outlook.
- Tie advice to the specific user profile and arbiter recommendation.
"""
    answer = call_gemini(prompt)
    return answer
