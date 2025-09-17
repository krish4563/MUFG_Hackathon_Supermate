SuperMate - AI Retirement Advisor 🚀
SuperMate is an intelligent retirement planning application that combines behavioral analysis, fraud detection, and portfolio optimization to provide personalized investment advice for superannuation (retirement) planning.
Features ✨

AI-Powered Chat Interface: Interactive conversation with Gemini AI for personalized retirement advice
Behavioral Analysis: User spending pattern clustering and profiling
Fraud Detection: Anomaly detection for suspicious transactions
Portfolio Simulation: Monte Carlo simulations for retirement planning across different risk profiles
Data Upload Support: Import transaction history and price data (CSV/XLSX)
Real-time Analysis: Integration of multiple AI agents for comprehensive financial insights

Architecture 🏗️
The application follows a multi-agent architecture:

BehaviorAgent: Analyzes user spending patterns using K-means clustering
FraudAgent: Detects anomalies in transaction data using Isolation Forest
PortfolioAgent: Runs Monte Carlo simulations for retirement projections
RAG System: Retrieval-Augmented Generation for contextual AI responses
Streamlit Frontend: User-friendly web interface

Installation 📦

Clone the repository

bashgit clone <repository-url>
cd supermate

Install dependencies

bashpip install -r requirements.txt

Set up environment variables
Create a .env file in the root directory:

envGEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here  # Optional
PINECONE_ENVIRONMENT=your_pinecone_env       # Optional
VECTOR_STORE=faiss  # or "pinecone"
Usage 🚀

Start the application

bashstreamlit run app.py

Complete onboarding

Enter personal details (age, retirement age, current balance)
Set monthly contribution and risk preferences
Upload transaction data (optional)
Upload price history data (optional)


Chat with SuperMate

Ask questions about retirement planning
Get personalized investment advice
Receive portfolio simulations and projections



File Structure 📁
├── app.py                 # Main Streamlit application
├── agents.py             # AI agent implementations
├── arbiter.py            # Agent output merger and decision engine
├── indexer.py            # Vector indexing for RAG (FAISS/Pinecone)
├── planner.py            # Monte Carlo simulation utilities
├── rag.py                # RAG implementation with Gemini AI
├── utils.py              # Data loading and processing utilities
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            # This file
Key Components 🔧
Agents (agents.py)

BehaviorAgent: Clusters users based on spending patterns
FraudAgent: Detects anomalous transactions
PortfolioAgent: Simulates retirement scenarios with multiple strategies:

Conservative (4% annual return, 6% volatility)
Balanced (7% annual return, 12% volatility)
Growth (10% annual return, 18% volatility)



RAG System (rag.py)

Integrates user profile, transaction data, and price history
Uses Google Gemini AI for contextual responses
Provides personalized retirement advice

Vector Search (indexer.py)

Supports both FAISS (local) and Pinecone (cloud) backends
Uses sentence-transformers for text embeddings
Enables semantic search for relevant financial information

Data Formats 📊
Transaction Data (CSV/XLSX)
Expected columns:

user_id: User identifier
amount: Transaction amount
date: Transaction date (optional)

Price History (CSV)
Expected columns:

date: Date column
close: Closing price

Configuration ⚙️
Environment Variables

GEMINI_API_KEY: Required for AI chat functionality
PINECONE_API_KEY: Optional, for cloud vector storage
PINECONE_ENVIRONMENT: Required if using Pinecone
VECTOR_STORE: Choose "faiss" (default) or "pinecone"

Risk Profiles
The system supports three investment strategies:

Conservative: Lower risk, stable returns
Balanced: Moderate risk and returns
Growth: Higher risk, potential for higher returns

API Integration 🔌
Google Gemini AI
The application uses Google's Gemini AI model for generating personalized retirement advice. Ensure you have:

A valid Gemini API key
Appropriate quotas and permissions

Pinecone (Optional)
For production deployments with large datasets, Pinecone provides scalable vector search:

Create a Pinecone account
Set up an index
Configure environment variables

Development 💻
Adding New Agents

Create agent class in agents.py
Implement required methods
Update arbiter.py to include new agent outputs
Modify RAG system to incorporate new insights

Extending Simulations

Add new strategy profiles in PortfolioAgent.STRATEGY_PROFILES
Update Monte Carlo parameters as needed
Enhance visualization in the frontend

Dependencies 📋
Main libraries:

Streamlit: Web application framework
Pandas/NumPy: Data manipulation and analysis
Scikit-learn: Machine learning algorithms
Sentence-transformers: Text embeddings
FAISS: Vector similarity search
Google GenerativeAI: AI chat functionality

See requirements.txt for complete list with versions.
Contributing 🤝

Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request

License 📄
[Add your license information here]
Support 💬
For questions and support:

Open an issue on GitHub
Contact the development team
Check the documentation


SuperMate - Making retirement planning intelligent and accessible! 💰📈
