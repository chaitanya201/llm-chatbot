
from langgraph.graph import MessagesState


class ChatState(MessagesState):
    prompt: str
    aiResponse: str
