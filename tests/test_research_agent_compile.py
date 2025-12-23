"""
Compilation tests for ResearchAgent.

This module tests that the ResearchAgent class and its dependencies
can be imported and instantiated without runtime errors.
"""

import os
from unittest.mock import patch

import pytest


def test_import_research_agent():
    """Test that ResearchAgent can be imported successfully."""
    try:
        from src.research_agent import ResearchAgent
        assert ResearchAgent is not None
    except ImportError as e:
        pytest.fail(f"Failed to import ResearchAgent: {e}")


def test_research_agent_instantiation():
    """Test that ResearchAgent can be instantiated."""
    # Mock environment variables to avoid actual API calls
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "ROOT_PATH": "/tmp/test",
            "FIRECRAWL_API_KEY": "test_firecrawl_key",
        },
    ):
        from src.research_agent import ResearchAgent

        agent = ResearchAgent()
        assert agent is not None
        assert agent.tavily_client is not None
        assert agent.mcp_client is not None
        assert agent.system_prompt is not None
        assert agent.agent is None  # Not initialized yet


def test_research_agent_custom_prompt():
    """Test that ResearchAgent accepts custom system prompt."""
    custom_prompt = "Custom research prompt"

    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "ROOT_PATH": "/tmp/test",
            "FIRECRAWL_API_KEY": "test_firecrawl_key",
        },
    ):
        from src.research_agent import ResearchAgent

        agent = ResearchAgent(system_prompt=custom_prompt)
        assert agent.system_prompt == custom_prompt


def test_research_agent_has_required_methods():
    """Test that ResearchAgent has all required methods."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "ROOT_PATH": "/tmp/test",
            "FIRECRAWL_API_KEY": "test_firecrawl_key",
        },
    ):
        from src.research_agent import ResearchAgent

        agent = ResearchAgent()

        # Check that all required methods exist
        assert hasattr(agent, "internet_search")
        assert hasattr(agent, "initialize")
        assert hasattr(agent, "research")
        assert callable(agent.internet_search)
        assert callable(agent.initialize)
        assert callable(agent.research)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
