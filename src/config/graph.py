from langgraph.graph import END, START, StateGraph

from config.state import ChatState
from config.tools import llm


def build_graph(checkpointer):
    builder = StateGraph(ChatState)

    builder.add_node("llm", llm)
    builder.add_edge(START, "llm")
    builder.add_edge("llm", END)

    return builder.compile(checkpointer=checkpointer)
