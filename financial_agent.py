import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools 
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Multi-Agent Financial Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for improved UI appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .agent-card h3 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    .agent-card p {
        color: #333333;
        margin: 0;
        line-height: 1.5;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    /* Improve text selection and highlighting visibility */
    ::selection {
        background-color: #1f77b4;
        color: white;
    }
    ::-moz-selection {
        background-color: #1f77b4;
        color: white;
    }
    /* Enhanced code block styling for better readability */
    .stCode {
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
    }
    /* Ensure proper contrast for highlighted text elements */
    mark {
        background-color: #fff3cd;
        color: #856404;
    }
    /* Fix sidebar text visibility issues */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize and configure AI agents with caching for performance
@st.cache_resource
def initialize_agents(max_tokens=300, temperature=0.1):
    """
    Create and configure the three AI agents used in the application.
    
    Args:
        max_tokens (int): Maximum number of tokens for model responses
        temperature (float): Controls randomness in responses (0.0 = deterministic)
    
    Returns:
        tuple: Contains websearch_agent, finance_agent, and multi_agent instances
    """
    # Create web search agent for real-time information gathering
    websearch_agent = Agent(
        name="Web search agent",
        role="Search the web for the information",
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=temperature
        ),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True
    )

    # Create financial agent for stock market analysis
    finance_agent = Agent(
        name="Financial Agent",
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=temperature
        ),
        tools=[YFinanceTools(
            stock_price=True, 
            analyst_recommendations=True, 
            stock_fundamentals=True,
            company_news=True, 
            historical_prices=True
        )],
        instructions=["Use Tables to display Data"],
        show_tool_calls=True,
        markdown=True
    )

    # Create multi-agent system combining both agents
    multi_agent = Agent(
        team=(websearch_agent, finance_agent),
        instructions=["Always include sources", "Use table to display the data"],
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=temperature
        ),
        show_tool_calls=True,
        markdown=True
    )
    
    return websearch_agent, finance_agent, multi_agent

# Display main application header
st.markdown('<h1 class="main-header">🤖 Multi-Agent Financial Assistant</h1>', unsafe_allow_html=True)

# Create sidebar for configuration and controls
with st.sidebar:
    st.header("🛠️ Agent Configuration")
    
    # Check if required API key is available
    if not os.getenv("GROQ_API_KEY"):
        st.error("⚠️ GROQ_API_KEY not found in environment variables!")
        st.info("Please add your GROQ API key to your .env file")
    else:
        st.success("✅ GROQ API Key loaded")
    
    st.divider()
    
    # Agent type selection dropdown
    agent_type = st.selectbox(
        "Select Agent Type",
        ["Multi-Agent (Recommended)", "Financial Agent Only", "Web Search Agent Only"],
        index=0
    )
    
    st.divider()
    
    # Model configuration settings
    st.subheader("⚙️ Model Settings")
    
    # Token limit slider with restricted maximum
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=500,
        value=300,
        step=50,
        help="Maximum number of tokens for the model response (limited to 500)"
    )
    
    # Temperature is fixed for consistent responses
    temperature = 0.1
    st.info("🌡️ Temperature: **0.1** (fixed for consistent responses)")
    
    # Display current token configuration
    st.info(f"🎯 Current token limit: **{max_tokens:,}** tokens")
    
    # Show token usage from previous response if available
    if 'last_response_tokens' in st.session_state:
        st.metric(
            "Last Response Tokens", 
            st.session_state.last_response_tokens,
            help="Estimated tokens used in the last response"
        )
    
    st.divider()
    
    # Quick action buttons for common queries
    st.subheader("🚀 Quick Actions")
    
    # Arrange quick action buttons in columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 AAPL Analysis"):
            st.session_state.quick_query = "Analyze Apple (AAPL) stock with latest news and analyst recommendations"
    
    with col2:
        if st.button("🏦 Market Overview"):
            st.session_state.quick_query = "Give me an overview of today's stock market performance"
    
    if st.button("💼 Tech Stocks Comparison"):
        st.session_state.quick_query = "Compare AAPL, GOOGL, MSFT, and TSLA stocks with analyst recommendations"
    
    if st.button("📰 Crypto News"):
        st.session_state.quick_query = "Latest cryptocurrency news and Bitcoin price analysis"

# Main application content area
try:
    # Get current configuration settings from sidebar
    current_max_tokens = max_tokens if 'max_tokens' in locals() else 300
    current_temperature = 0.1  # Fixed temperature for consistent responses
    
    # Initialize agents with current settings
    websearch_agent, finance_agent, multi_agent = initialize_agents(current_max_tokens, current_temperature)
    
    # Display agent capability cards in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h3>🌐 Web Search Agent</h3>
            <p>Searches the web for current information and news using DuckDuckGo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h3>📊 Financial Agent</h3>
            <p>Provides stock analysis, prices, fundamentals, and analyst recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <h3>🤝 Multi-Agent</h3>
            <p>Combines both agents for comprehensive financial analysis with web research</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Query input
    st.subheader("💬 Ask Your Question")
    
    # Check for quick query
    default_query = ""
    if hasattr(st.session_state, 'quick_query'):
        default_query = st.session_state.quick_query
        del st.session_state.quick_query
    
    user_query = st.text_area(
        "Enter your financial or research question:",
        value=default_query,
        height=100,
        placeholder="e.g., 'Summarize analyst recommendations and share the latest news for Tesla (TSLA)'"
    )
    
    # Example queries
    with st.expander("💡 Example Queries"):
        st.markdown("""
        **Financial Analysis:**
        - "Analyze Apple stock performance and show analyst recommendations"
        - "Compare Tesla and Ford stock fundamentals"
        - "What are the latest analyst ratings for Microsoft?"
        
        **Market Research:**
        - "Latest news about cryptocurrency regulations"
        - "Current market sentiment on tech stocks"
        - "Recent developments in the AI industry"
        
        **Combined Analysis:**
        - "Tesla stock analysis with latest company news"
        - "Meta financial performance and recent announcements"
        - "Amazon earnings report and analyst reactions"
        """)
    
    # Process query
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Analysis", type="primary"):
            if user_query:
                with st.spinner("🤖 Agents are working on your request..."):
                    try:
                        # Select appropriate agent
                        if agent_type == "Multi-Agent (Recommended)":
                            selected_agent = multi_agent
                        elif agent_type == "Financial Agent Only":
                            selected_agent = finance_agent
                        else:
                            selected_agent = websearch_agent
                        
                        # Get response
                        response = selected_agent.run(user_query)
                        
                        # Estimate token usage (rough approximation)
                        if hasattr(response, 'content'):
                            estimated_tokens = len(str(response.content).split()) * 1.3  # Rough estimation
                            st.session_state.last_response_tokens = int(estimated_tokens)
                        
                        # Display results
                        st.divider()
                        st.subheader("📋 Analysis Results")
                        
                        # Token usage info
                        if 'last_response_tokens' in st.session_state:
                            col_token1, col_token2, col_token3 = st.columns(3)
                            with col_token1:
                                st.metric("Estimated Tokens Used", f"{st.session_state.last_response_tokens:,}")
                            with col_token2:
                                st.metric("Token Limit", f"{current_max_tokens:,}")
                            with col_token3:
                                percentage_used = (st.session_state.last_response_tokens / current_max_tokens) * 100
                                st.metric("Usage %", f"{percentage_used:.1f}%")
                        
                        # Create tabs for better organization
                        tab1, tab2 = st.tabs(["📊 Response", "🔧 Agent Details"])
                        
                        with tab1:
                            if hasattr(response, 'content'):
                                st.markdown(response.content)
                            else:
                                st.markdown(str(response))
                        
                        with tab2:
                            st.info(f"**Agent Used:** {selected_agent.name}")
                            
                            # Model settings display
                            st.subheader("🎛️ Model Configuration")
                            config_col1, config_col2 = st.columns(2)
                            with config_col1:
                                st.write(f"**Max Tokens:** {current_max_tokens:,}")
                                st.write(f"**Model:** llama-3.3-70b-versatile")
                            with config_col2:
                                st.write(f"**Temperature:** {current_temperature} (fixed)")
                                st.write(f"**Provider:** Groq")
                            
                            if hasattr(response, 'tool_calls') and response.tool_calls:
                                st.subheader("🛠️ Tools Used")
                                for tool_call in response.tool_calls:
                                    st.code(f"Tool: {tool_call.get('function', {}).get('name', 'Unknown')}")
                    
                    except Exception as e:
                        st.error(f"❌ Error occurred: {str(e)}")
                        st.info("Please check your API keys and try again.")
            else:
                st.warning("⚠️ Please enter a question first!")

# Handle initialization errors gracefully
except Exception as e:
    st.error(f"❌ Failed to initialize agents: {str(e)}")
    st.info("""
    **Troubleshooting:**
    1. Make sure you have installed all required packages:
       ```
       pip install streamlit phidata groq yfinance duckduckgo-search python-dotenv
       ```
    2. Ensure your .env file contains:
       ```
       GROQ_API_KEY=your_groq_api_key_here
       ```
    3. Check that all imports are working correctly.
    """)

# Application footer with attribution
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 Multi-Agent Financial Assistant powered by Groq and Phi Framework</p>
    <p>Built with Streamlit • Financial data from Yahoo Finance • Web search via DuckDuckGo</p>
</div>
""", unsafe_allow_html=True)