from agno.agent import Agent
from lib.model import get_model
from agno.tools.yfinance import YFinanceTools


agent = Agent(
    name="my-agent",
    model=get_model(),#"google:gemini-2.0-flash",#OpenAIResponses(id="gpt-5.2"),
    tools=[
        YFinanceTools(),#stock_price=True, analyst_recommendations=True, company_info=True),
    ],
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions="Format your response using markdown and use tables to display data where possible.",
)