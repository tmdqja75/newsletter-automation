import os
from typing import Literal, Optional

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware
from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from tavily import AsyncTavilyClient

from .prompt import DEFAULT_RESEARCH_INSTRUCTIONS

load_dotenv()


class ResearchAgent:
    """Research agent for newsletter articles that can be used in parallel for multiple topics."""

    

    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize a research agent instance.

        Args:
            system_prompt: Optional custom system prompt. If not provided, uses default.
        """
        self.tavily_client = AsyncTavilyClient(api_key=os.environ["TAVILY_API_KEY"])
        self.mcp_client = MultiServerMCPClient(
            {
                "context7": {
                    "transport": "stdio",
                    "command": "docker",
                    "args": ["run", "-i", "--rm", "context7-mcp:latest"],
                }
            }
        )
        self.system_prompt = system_prompt or DEFAULT_RESEARCH_INSTRUCTIONS
        self.agent = None

    async def internet_search(
        self,
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ):
        """Run a web search"""
        return await self.tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    async def initialize(self):
        """Initialize the agent with tools. Must be called before using the agent."""
        tools = await self.mcp_client.get_tools()

        # Wrap internet_search as a proper async tool
        internet_search_tool = StructuredTool.from_function(
            coroutine=self.internet_search,
            name="internet_search",
            description="Run a web search to find information on the internet. Use this to find current information, news, and research topics."
        )
        
        # file_backend = FilesystemBackend(
        #     root_dir=".", virtual_mode=True
        # )

        self.agent = create_deep_agent(
            tools=[internet_search_tool] + list(tools),
            backend=FilesystemBackend(root_dir=os.environ["ROOT_PATH"], virtual_mode=True),
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
        return await self.agent.ainvoke({"messages":query})

