from langgraph.graph import END, START, StateGraph

from config.state import ChatState
from config.tools import decisionMaker, generalClarityOfThought, generalTopicEssay, llm


def build_graph(checkpointer):
    builder = StateGraph(ChatState)

    builder.add_node("generalTopicEssay", generalTopicEssay)
    builder.add_node("generalClarityOfThought", generalClarityOfThought)
    builder.add_node("decisionMaker", decisionMaker)
    builder.add_edge("generalTopicEssay", "generalClarityOfThought")
    builder.add_edge("generalClarityOfThought", "decisionMaker")
    builder.add_edge(START, "generalTopicEssay")
    builder.add_edge("decisionMaker", END)

    return builder.compile(checkpointer=checkpointer)
