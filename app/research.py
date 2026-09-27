import os

from dotenv import load_dotenv
from tavily import TavilyClient
from app.schemas import Source
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(task: str):

    response = tavily.search(
        query=task,
        search_depth="advanced",
        max_results=5
    )

    sources = []

    for result in response["results"]:

        source = Source(
            title=result["title"],
            url=result["url"],
            content=result["content"]
        )

        sources.append(source)

    return sources

def research_all_tasks(tasks):

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = executor.map(search_web, tasks)

    research_results = []

    for task, sources in zip(tasks, results):

        research_results.append(
            {
                "task": task,
                "sources": sources
            }
        )

    return research_results