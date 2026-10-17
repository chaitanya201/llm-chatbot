from config.gemini import gemini_model
from config.state import AnalysisResult, ChatState, DecisionResult, EssayResponse


def llm(state: ChatState):
    prompt = state["prompt"]
    messages = state.get("messages", [])
    result = gemini_model.invoke([
        *messages,
        {"role": "human", "content": prompt},
    ])
    response = result.content[-1]["text"]
    return {
        "aiResponse": response,
        "messages": [
            *messages,
            {"role": "human", "content": prompt},
            {"role": "assistant", "content": response},
        ],
    }


def generalTopicEssay (state: ChatState):
    struc_model = gemini_model.with_structured_output(EssayResponse)
    result:EssayResponse = struc_model.invoke([
        {
            "role": "system",
            "content":"Write essay on given topic by user. keep its size max only 200 tokens"
        },
        {
            "role": "human",
            "content": state["prompt"]
        }
    ])

    return {"essay_response": result.essay}

def generalClarityOfThought (state: ChatState):
    struc_model:AnalysisResult = gemini_model.with_structured_output(AnalysisResult)
    
    result = struc_model.invoke([
        {
            "role": "system",
            "content":""" 
            You are an expert essay evaluator. Evaluate the essay exclusively for **clarity of thought**.

Assess the following:
- How clearly the writer communicates the central idea or thesis.
- Whether ideas are logically organized and connected.
- Whether arguments are coherent, focused, and easy to follow.
- Whether the essay avoids contradictions, ambiguity, and unnecessary repetition.
- Whether the conclusion follows logically from the discussion.

Assign a score between 0 and 10:
- 0–2: Thoughts are extremely unclear, disorganized, or incoherent.
- 3–4: Ideas are difficult to follow and poorly connected.
- 5–6: Main ideas are understandable but have some organizational or logical weaknesses.
- 7–8: Ideas are clear, well-organized, and logically connected.
- 9–10: Exceptionally clear, coherent, focused, and logically structured.

Do not evaluate grammar, vocabulary, or writing style unless they directly affect clarity of thought.

Return:
- `score`: A numeric value from 0 to 10, allowing decimal values.
- `response`: Concise text containing specific observations that justify the score, including strengths and areas for improvement where applicable.

Be objective, consistent, and evidence-based. Do not reward an essay merely for being long or using complex vocabulary. Evaluate only the essay provided.
            
            keep its size max only 200 tokens
            """
        },
        {
            "role": "ai",
            "content": state["essay_response"]
        }
    ])
    
    return {"clarity_of_thought_response": result}

def decisionMaker(state: ChatState):
    struc_model = gemini_model.with_structured_output(DecisionResult)

    result:AnalysisResult = struc_model.invoke([
            {
                "role": "system",
                "content":"""
                You are an expert essay evaluation decision maker. Your task is to review an essay analysis and make a final decision to either PASS or FAIL the essay.

Evaluate the essay based on these dimensions:
1. Clarity of thought
2. Depth of analysis
3. Language understanding

Each dimension has a score between 0 and 10, along with supporting feedback.

### Decision rules

- **PASS:** The essay demonstrates an acceptable level of clarity, analytical depth, and language understanding.
- **FAIL:** The essay has significant weaknesses in one or more dimensions that make it unsuitable for passing.

Use the following scoring criteria:
- Clarity of thought: minimum 5/10
- Depth of analysis: minimum 5/10
- Language understanding: minimum 5/10

An essay passes only if **all three dimensions score at least 5/10**. If any dimension scores below 5, the final decision must be FAIL.

### Instructions

- Base your decision strictly on the provided scores and supporting feedback.
- Do not change or recalculate the dimension scores.
- Explain the decision using specific evidence from the feedback.
- Identify the strengths of the essay if it passes.
- If it fails, identify the specific weaknesses that caused the failure and what the writer should improve.
- Do not introduce criteria that are not specified above.
- Be consistent, objective, and fair.
- Return exactly one decision: `PASS` or `FAIL`.

### Output format

Return a structured object containing:
- `decision`: Either `"PASS"` or `"FAIL"`.
- `reason`: concise text why the essay passed or failed.

Do not include any additional text outside the output object.
                keep its size max only 200 tokens"""
            },
            {
                "role": "ai",
                "content": state["clarity_of_thought_response"].model_dump_json()
            }
        ])
    
    return {"final_evaluation": result}
    
