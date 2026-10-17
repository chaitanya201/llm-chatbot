from config.gemini import gemini_model
from config.state import ChatState


def llm(state: ChatState):
    print("state is ", state)
    prompt = state['prompt']
    result = gemini_model.invoke([
        *state["messages"],
        {"role": "human", "content": prompt},
    ])
    print("llm response is --------------------------------------", result)
    state["messages"].append( {"role": "human", "content": prompt},)
    state["messages"].append({"role":"assistant","content":result.content[-1]['text']})
    print("updated messages----------------------------------------------", state["messages"])
    return {"aiResponse": result.content[-1]['text'], "messages": state["messages"] }
