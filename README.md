# 🤖 Multi-Agent Financial Assistant

A **Proof of Concept (POC)** demonstrating how AI agents work together for financial analysis and web search.
You can check it out on https://ai-financial-agent-poc.streamlit.app/ (The backend is not deployed so it might not run all the time but you can see how the UI looks like)

> **Note**: This is a demonstration project to showcase AI agent capabilities and workflows.

## 🚀 Quick Setup

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd multi-agent-financial-assistant
pip install -r requirements.txt
```

### Step 2: Create API Key for Phi Data
1. Go to [Phi Data Platform](https://phidata.app/)
2. Sign up and create an API key
3. Copy the API key

### Step 3: Create API Key for Groq
1. Go to [Groq Console](https://console.groq.com/)
2. Sign up and create an API key
3. Copy the API key

### Step 4: Setup Environment
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
PHI_API_KEY=your_phi_api_key_here
```

## 🏃 Run the Application

### Option 1: Streamlit Web App
```bash
streamlit run Financial_agent.py
```

### Option 2: Phi Dashboard
```bash
python playground.py
```

## 📋 Requirements
```
streamlit>=1.28.0
phidata
groq
yfinance
duckduckgo-search
python-dotenv
```

---
**Built with Phi Data • Powered by Groq**
