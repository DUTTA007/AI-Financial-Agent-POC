from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools 
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
load_dotenv()

# # For Open API
# from dotenv import load_dotenv
# import os
# load_dotenv()  # Loads from .env file
# api_key = os.getenv("OPENAI_API_KEY")


# Websearch Agent

websearch_agent = Agent(
    name = "Web search agent",
    role = "Search the web for the information",
    model = Groq(id="llama-3.3-70b-versatile"),
    tools = [DuckDuckGo()],
    instructions = ["Always include sources"],
    show_tool_calls = True,
    markdown = True
)

# Financial Agent 

finance_agent = Agent(
    name = "Fiancial Agent",
    model = Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True, historical_prices= True)],
    instructions = ["Use Tables to display Data"],
    show_tool_calls = True,
    markdown = True
)

multi_agent = Agent(
    team = (websearch_agent, finance_agent),
    instructions = ["Always include sources","Use table to display the data"],
    model = Groq(id="llama-3.3-70b-versatile"),
    show_tool_calls = True,
    markdown = True
)

multi_agent.print_response("Summarize analyst recommendation and share the latest news for Meta")
