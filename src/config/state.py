
from langgraph.graph import MessagesState
from typing import TypedDict

from typing import Literal

from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    score: float = Field(ge=0, le=10)
    response:str = Field(
        description="response of AI model."
    )
    

class EssayResponse(BaseModel):
    essay: str = Field(
        description="The generated essay, with a maximum length of 200 tokens."
    )

class DecisionResult(BaseModel):
    decision: Literal["PASS", "FAIL"]
    reason: str

class ChatState(MessagesState):
    prompt: str
    aiResponse: str
    essay_response: str
    clarity_of_thought_response: AnalysisResult
    depth_analysis_response: AnalysisResult
    language_understanding_response: AnalysisResult
    final_evaluation: DecisionResult
