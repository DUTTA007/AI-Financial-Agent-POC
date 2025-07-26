from phi.agent import agent
from phi.model.groq import groq
from phi.tools.yfinance import YFinanceTools 
from phi.tools.duckduckgo import DuckDuckGo


# Websearch Agent

websearch_agent = agent(
    name = "Web search agent",
    role = "Search the web for the information",
    model = groq(id="compound-beta-kimi"),
    tools = [DuckDuckGo()],
    instruction = ["Always include sources"],
    show_tool_calls = True,
    markdown = True
)

# Financial Agent 

finance_agent = agent(
    name = "Fiancial Agent",
    model = groq(id="compound-beta-kimi"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True, historical_prices= True)],
    instruction = ["Use Tables to display Data"],
    show_tool_calls = True,
    markdown = True
)


multi_agent = Agent(
    team = (websearch_agent, finance_agent),
    instructions = ["Always include sources","Use table to display the data"],
    show_tool_calls = True,
    markdown = True
)

multi_agent.print_response("Summarize analyst recommendation and share the latest news for NV")
