# SuperMate - AI Retirement Advisor 🚀

SuperMate is an intelligent retirement planning application that combines behavioral analysis, fraud detection, and portfolio optimization to provide personalized investment advice for superannuation (retirement) planning.

🌐 **Live Demo**: [http://supermate.streamlit.app/](http://supermate.streamlit.app/)

## Features ✨

- **AI-Powered Chat Interface**: Interactive conversation with Gemini AI for personalized retirement advice
- **Behavioral Analysis**: User spending pattern clustering and profiling
- **Fraud Detection**: Anomaly detection for suspicious transactions
- **Portfolio Simulation**: Monte Carlo simulations for retirement planning across different risk profiles
- **Data Upload Support**: Import transaction history and price data (CSV/XLSX)
- **Real-time Analysis**: Integration of multiple AI agents for comprehensive financial insights

## Architecture 🏗️

The application follows a multi-agent architecture:

- **BehaviorAgent**: Analyzes user spending patterns using K-means clustering
- **FraudAgent**: Detects anomalies in transaction data using Isolation Forest
- **PortfolioAgent**: Runs Monte Carlo simulations for retirement projections
- **RAG System**: Retrieval-Augmented Generation for contextual AI responses
- **Streamlit Frontend**: User-friendly web interface

## Installation 📦

1. **Clone the repository**

```bash
git clone <repository-url>
cd supermate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
   Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here  # Optional
PINECONE_ENVIRONMENT=your_pinecone_env       # Optional
VECTOR_STORE=faiss  # or "pinecone"
```

## Usage 🚀

### Option 1: Use Live Demo

Visit [supermate.streamlit.app](http://supermate.streamlit.app/) to try the application instantly without any setup!

### Option 2: Run Locally

1. **Start the application**

```bash
streamlit run app.py
```

2. **Complete onboarding**

   - Enter personal details (age, retirement age, current balance)
   - Set monthly contribution and risk preferences
   - Upload transaction data (optional)
   - Upload price history data (optional)

3. **Chat with SuperMate**
   - Ask questions about retirement planning
   - Get personalized investment advice
   - Receive portfolio simulations and projections

## File Structure 📁

```
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
```

## Key Components 🔧

### Agents (`agents.py`)

- **BehaviorAgent**: Clusters users based on spending patterns
- **FraudAgent**: Detects anomalous transactions
- **PortfolioAgent**: Simulates retirement scenarios with multiple strategies:
  - Conservative (4% annual return, 6% volatility)
  - Balanced (7% annual return, 12% volatility)
  - Growth (10% annual return, 18% volatility)

### RAG System (`rag.py`)

- Integrates user profile, transaction data, and price history
- Uses Google Gemini AI for contextual responses
- Provides personalized retirement advice

### Vector Search (`indexer.py`)

- Supports both FAISS (local) and Pinecone (cloud) backends
- Uses sentence-transformers for text embeddings
- Enables semantic search for relevant financial information

## Data Formats 📊

### Transaction Data (CSV/XLSX)

Expected columns:

- `user_id`: User identifier
- `amount`: Transaction amount
- `date`: Transaction date (optional)

### Price History (CSV)

Expected columns:

- `date`: Date column
- `close`: Closing price

## Configuration ⚙️

### Environment Variables

- `GEMINI_API_KEY`: Required for AI chat functionality
- `PINECONE_API_KEY`: Optional, for cloud vector storage
- `PINECONE_ENVIRONMENT`: Required if using Pinecone
- `VECTOR_STORE`: Choose "faiss" (default) or "pinecone"

### Risk Profiles

The system supports three investment strategies:

- **Conservative**: 4% annual return, 6% volatility - Lower risk, stable returns
- **Balanced**: 7% annual return, 12% volatility - Moderate risk and returns
- **Growth**: 10% annual return, 18% volatility - Higher risk, potential for higher returns

## API Integration 🔌

### Google Gemini AI

The application uses Google's Gemini AI model for generating personalized retirement advice. Ensure you have:

1. A valid Gemini API key
2. Appropriate quotas and permissions

### Pinecone (Optional)

For production deployments with large datasets, Pinecone provides scalable vector search:

1. Create a Pinecone account
2. Set up an index
3. Configure environment variables

## Development 💻

### Adding New Agents

1. Create agent class in `agents.py`
2. Implement required methods
3. Update `arbiter.py` to include new agent outputs
4. Modify RAG system to incorporate new insights

### Extending Simulations

1. Add new strategy profiles in `PortfolioAgent.STRATEGY_PROFILES`
2. Update Monte Carlo parameters as needed
3. Enhance visualization in the frontend

## Dependencies 📋

Main libraries:

- **Streamlit**: Web application framework
- **Pandas/NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **Sentence-transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **Google GenerativeAI**: AI chat functionality

See `requirements.txt` for complete list with versions.

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

[Add your license information here]

## Support 💬

For questions and support:

- Open an issue on GitHub
- Contact the development team
- Check the documentation

---

**SuperMate** - Making retirement planning intelligent and accessible! 💰📈
