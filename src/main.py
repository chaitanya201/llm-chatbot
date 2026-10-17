from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from config.checkpointer import postgres_checkpointer
from config.graph import build_graph
from router.chat import chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with postgres_checkpointer() as checkpointer:
        app.state.graph = build_graph(checkpointer)
        yield


app = FastAPI(lifespan=lifespan)


app.include_router(chat_router)


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}



def main():
    uvicorn.run("main:app",reload=True)
