# Parallel Research (Multiple Topics)

import asyncio

from src.research_agent import ResearchAgent


async def main():
    topics = [
        "Research about langchain's new python package 'deepagents', introduce what it is, how it is different from langchain and langgraph,  and use cases. Do not include example codes.",
        
    ]

    # Create separate agent for each topic
    agents = [ResearchAgent() for _ in topics]

    # Research all topics in parallel
    results = await asyncio.gather(*[
        agent.research(topic) for agent, topic in zip(agents, topics)
    ])

    # Process results
    for topic, result in zip(topics, results):
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print(f"{'='*60}")
        print(result)

asyncio.run(main())