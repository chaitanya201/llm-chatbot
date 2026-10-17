
from fastapi import APIRouter, Request
from pydantic import BaseModel

chat_router = APIRouter(prefix="/chat", tags=['chat'])

class ChatData(BaseModel):
    prompt: str

@chat_router.post('')
def start_workflow(data: ChatData, request: Request):
    
    res = request.app.state.graph.invoke({'prompt': data.prompt},{'configurable':{
        "thread_id": "test_3"
    }})
    print("values", request.app.state.graph.get_state({'configurable':{
        "thread_id": "test_3"
    }}).values)
    return res