from agents import build_search_agent, build_search_reader_agent, writer_chain, critic_chain
from rich import print

def run_research_pipeline(topic: str) -> dict:

    state = {}

    #search agent working:
    print("\n"+ "="*50)
    print("Step 1 -- search agent is working--")
    print("\n"+ "="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content

    print("\n Search Result", state["search_results"])

    #step 2 -- reader agent:

    print("\n"+ "="*50)
    print("Step 1 -- Reader agent is working--")
    print("\n"+ "="*50)

    reader_agent = build_search_reader_agent()
    reader_agent.invoke({
        "messages":[("user",
            f"Based on the following search reuslts about '{topic}',"
            f"pick the most relevant URL and scrape it for the depper content. \n\n"
            f"Search Results: \n{state['search_results'][:800]}")]
    })

    state['scraped_content'] = search_result['messages'][-1].content

    print("\nscraped content: \n", state["scraped_content"])

    #Step-3
    print("\n"+ "="*50)
    print("Step 1 -- Writer agent is drafting--")
    print("\n"+ "="*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n Final Report\n", state['report'])

    #critic report:

    print("\n"+ "="*50)
    print("Step 1 -- Critics are reviewing the report--")
    print("\n"+ "="*50)

    state['feedback'] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n Cirtic Report\n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\nEnter your Research Topic: ")
    run_research_pipeline(topic)