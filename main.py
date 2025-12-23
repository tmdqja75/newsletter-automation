# Parallel Research (Multiple Topics)

import asyncio
import os
from datetime import datetime, timedelta
from pathlib import Path

from src.research_agent import ResearchAgent


def get_next_wednesday():
    """Get the date of the next Wednesday in YYYYMMDD format."""
    today = datetime.now()
    # Wednesday is weekday 2 (Monday=0, Tuesday=1, Wednesday=2, ...)
    days_ahead = 2 - today.weekday()

    # If today is Wednesday or later in the week, get next week's Wednesday
    if days_ahead <= 0:
        days_ahead += 7

    next_wednesday = today + timedelta(days=days_ahead)
    return next_wednesday.strftime("%Y%m%d")


def concatenate_articles():
    """Concatenate all markdown files in articles/ directory and save to dated directory."""
    root_path = Path(os.environ["ROOT_PATH"])
    articles_dir = root_path / "articles"

    # Find all markdown files in articles/ directory (not in subdirectories)
    md_files = sorted(articles_dir.glob("*.md"))

    if not md_files:
        print("No markdown files found in articles/ directory")
        return

    # Read and concatenate all markdown files
    concatenated_content = []
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            concatenated_content.append(content)

    # Join with markdown divider
    final_content = "\n\n---\n\n".join(concatenated_content)

    # Get next Wednesday date
    next_wednesday = get_next_wednesday()

    # Create directory for the dated newsletter
    output_dir = articles_dir / next_wednesday
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save concatenated file
    output_file = output_dir / "newsletter.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"\n{'='*60}")
    print(f"Newsletter created successfully!")
    print(f"{'='*60}")
    print(f"Location: {output_file}")
    print(f"Articles combined: {len(md_files)}")
    print(f"Output directory: {output_dir}")


async def main():
    topics = [
        # "Research about langchain's new python package 'deepagents', introduce what it is, how it is different from langchain and langgraph,  and use cases. Do not include example codes.",
        "Get the content of this site and write an article about a16z consultant's prediction on AI and AI Agents. Always include who made which claim. Keep in mind that there are some claims that are not related to AI or AI Agents./nhttps://a16z.com/newsletter/big-ideas-2026-part-1/,\nhttps://a16z.com/newsletter/big-ideas-2026-part-2/"
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

    # Concatenate all articles into a single newsletter file
    concatenate_articles()

asyncio.run(main())