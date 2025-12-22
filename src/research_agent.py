import os
from typing import Literal, Optional
from tavily import TavilyClient
from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


class ResearchAgent:
    """Research agent for newsletter articles that can be used in parallel for multiple topics."""

    DEFAULT_RESEARCH_INSTRUCTIONS = """You are an expert researcher for newsletter article. Your job is to conduct thorough research and then write a polished news article that are informative but easy to read even for non-professional.

You have access to an internet search tool and github tool as your primary means of gathering information.

If the user request contains the url to

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.


## `github_search`
Use this to run a github repository search
"""

    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize a research agent instance.

        Args:
            system_prompt: Optional custom system prompt. If not provided, uses default.
        """
        self.tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
        self.mcp_client = MultiServerMCPClient(
            {
                "context7": {
                    "transport": "stdio",
                    "command": "docker",
                    "args": ["run", "-i", "--rm", "context7-mcp"],
                }
            }
        )
        self.system_prompt = system_prompt or self.DEFAULT_RESEARCH_INSTRUCTIONS
        self.agent = None

    def internet_search(
        self,
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ):
        """Run a web search"""
        return self.tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    async def initialize(self):
        """Initialize the agent with tools. Must be called before using the agent."""
        tools = await self.mcp_client.get_tools()
        print(f"Loaded MCP tools: {tools}")
        self.agent = create_deep_agent(
            tools=[self.internet_search] + list(tools),
            system_prompt=self.system_prompt
        )
        return self.agent

    async def research(self, query: str):
        """
        Conduct research on a given query.

        Args:
            query: The research query or topic

        Returns:
            Research results from the agent
        """
        if self.agent is None:
            await self.initialize()
        return await self.agent.run(query)

