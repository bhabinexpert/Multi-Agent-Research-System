from langchain.tools  import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str) -> str:
    """Search the web for recent and most reliable information on a topic. Returns tiltls, urls, snippets.
    """
    results = tavily.search(query=query,max_results=5)

    output =[]
    for r in results['results']:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippets: {r['content'] [:300]}\n"
        )

    return "\n-------\n".join(output)

@tool
def scrape_url(url: str) -> str:
    """Fetch a web page and return its readable text content."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style","nav","footer" "noscript"]):
            element.decompose()
        return soup.get_text(" ", strip=True)[:3000]

    except Exception as e:
        return f"could not scrape URL: {str(e)}"

# print(web_search.invoke("What is the recent nes on wars?"))



