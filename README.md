# SuperMate - Your AI-Powered Retirement Advisor 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://supermate.streamlit.app/)

SuperMate is an intelligent retirement planning application that combines behavioral analysis, fraud detection, and portfolio optimization to provide personalized investment advice for your superannuation (retirement) fund.

![SuperMate Demo GIF](https://your-image-hosting-url/supermate-demo.gif)

🌐 **Live Demo**: **[Try SuperMate Now!](http://supermate.streamlit.app/)**

---

### 🤔 Why SuperMate?

Retirement planning is often confusing, impersonal, and riddled with generic advice. SuperMate tackles this by providing a hyper-personalized experience. Our multi-agent AI system analyzes your unique financial behavior to deliver insights that go beyond simple calculators, helping you build a robust and realistic retirement plan.

### ✨ Features

- **AI-Powered Chat Interface**: Have an interactive conversation with Gemini AI for truly personalized retirement advice.
- **Behavioral Analysis**: Understand your own spending habits through automated user clustering and profiling.
- **Fraud Detection**: Protect your savings with an anomaly detection engine that flags suspicious transactions.
- **Portfolio Simulation**: Visualize your future with Monte Carlo simulations across different risk profiles.
- **Data Upload Support**: Easily import your transaction history and market data (CSV/XLSX).
- **Real-time Analysis**: Benefit from the synergy of multiple AI agents working together for comprehensive financial insights.

### 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend/ML**: Pandas, NumPy, Scikit-learn
- **AI/LLM**: Google Generative AI (Gemini)
- **Vector Search**: FAISS / Pinecone
- **Embeddings**: Sentence-Transformers

### 🏗️ Architecture

The application follows a multi-agent architecture where different AI agents collaborate to provide holistic advice:

- **`BehaviorAgent`**: Analyzes user spending patterns using K-means clustering.
- **`FraudAgent`**: Detects anomalies in transaction data using an Isolation Forest model.
- **`PortfolioAgent`**: Runs Monte Carlo simulations for retirement projections.
- **`RAG System`**: Provides context-aware, accurate responses using Retrieval-Augmented Generation.
- **`Streamlit Frontend`**: A user-friendly and interactive web interface.

---

### 📦 Installation

Get SuperMate running on your local machine.

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/supermate.git](https://github.com/your-username/supermate.git)
    cd supermate
    ```

2.  **Create and activate a virtual environment** (Recommended)
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GEMINI_API_KEY="your_gemini_api_key_here"
    PINECONE_API_KEY="your_pinecone_api_key_here"  # Optional
    PINECONE_ENVIRONMENT="your_pinecone_env"       # Optional
    VECTOR_STORE="faiss" # or "pinecone"
    ```

---

### 🚀 Usage

#### Option 1: Use the Live Demo
The easiest way to get started is to visit the live application:
[supermate.streamlit.app](http://supermate.streamlit.app/)

#### Option 2: Run Locally
1.  **Start the application**
    ```bash
    streamlit run app.py
    ```

2.  **Complete the onboarding process in your browser:**
    - Enter personal details (age, retirement age, current balance).
    - Set your monthly contribution and risk preferences.
    - Upload your transaction data (optional).
    - Upload price history data for simulations (optional).

3.  **Chat with SuperMate!**
    - Ask questions about retirement planning.
    - Get personalized investment advice.
    - Request portfolio simulations and see your financial future projected.

---

### 📁 File Structure
```
supermate/
├── .gitignore          # Specifies files and folders for Git to ignore
├── app.py              # 🚀 Main entry point for the Streamlit application
├── agents.py           # 🧠 Core logic for all AI agents (Behavior, Fraud, Portfolio)
├── arbiter.py          # ⚖️ Decision engine to merge and prioritize outputs from agents
├── indexer.py          # 🗂️ Handles vector indexing and searching (FAISS/Pinecone)
├── planner.py          # 📈 Monte Carlo simulation and financial planning utilities
├── rag.py              # 💬 RAG implementation connecting Gemini to the vector store
├── utils.py            # 🛠️ Helper functions for data loading, cleaning, etc.
├── requirements.txt    # 📦 List of Python dependencies for the project
├── .env.example        # 📝 Template for environment variables
├── README.md           # 📄 You are here!
├── LICENSE             # 📜 Project license file (e.g., MIT)
└── data/
    └── sample_transactions.csv   # Example transaction data for new users
    └── sample_price_history.csv  # Example price history data for simulations
```

*(Note: I added `.env.example` which is a good practice)*

---

### 🔧 Key Components

#### Agents (`agents.py`)
- **BehaviorAgent**: Clusters users based on spending patterns.
- **FraudAgent**: Detects anomalous transactions.
- **PortfolioAgent**: Simulates retirement scenarios with multiple strategies:
  - **Conservative**: 4% annual return, 6% volatility
  - **Balanced**: 7% annual return, 12% volatility
  - **Growth**: 10% annual return, 18% volatility

#### RAG System (`rag.py`)
Integrates your profile, transaction data, and price history to provide contextual, data-driven responses using Google Gemini AI.

#### Vector Search (`indexer.py`)
Supports both **FAISS** (local) and **Pinecone** (cloud) backends for efficient semantic search over financial information.

---

### 📊 Data Formats

#### Transaction Data (CSV/XLSX)
- `user_id`: User identifier
- `amount`: Transaction amount
- `date`: Transaction date (optional)

#### Price History (CSV)
- `date`: Date column
- `close`: Closing price of the asset

---

### 🤝 Contributing

Contributions are welcome! We are excited to see how the community can help improve SuperMate.

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/your-awesome-feature`).
3.  Make your changes and commit them (`git commit -m 'Add some awesome feature'`).
4.  Push to the branch (`git push origin feature/your-awesome-feature`).
5.  Open a Pull Request.

Please check the [GitHub Issues](https://github.com/your-username/supermate/issues) for bugs or feature requests.

### 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### 💬 Support

For questions, support, or feedback, please **[open an issue on GitHub](https://github.com/your-username/supermate/issues/new)**.

---
**SuperMate** - Making retirement planning intelligent and accessible! 💰📈
