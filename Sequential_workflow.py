import os
from typing import TypedDict

class pipelineState(TypedDict):
    raw_input:str
    edited_text:str
    script_text:str
    final_output:str

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-120b",temperature=0.7)
#nodes take states as input, modify them and send as output
def editor_node(state:pipelineState)->dict:
    """step 1 : clean grammar, remove typos and clean the tone"""

    prompt = (
    "You are an expert copyeditor. Clean up the following raw text. "
    "Fix any grammatical errors, spelling mistakes, and smooth out the transitions "
    "while keeping the core message intact. Return only the edited text.\n\n"
    f"Text:\n{state['raw_input']}"
    )

    response=llm.invoke(prompt)

    return {"edited_text":response.content.strip()}

def scriptwriter_node(state:pipelineState)->dict:
    """step 2 : formats the clean text into an engaging video script style"""

    prompt = (
    "You are a charismatic Youtube content creator.Take this edited text and transform it into highly "
    "engaging, punchy, conversational video script hook. Make it sound like a real person speaking passionately"
    "Return only the script content.\n\n"
    f"Text:\n{state['edited_text']}"
    )

    response=llm.invoke(prompt)

    return {"script_text":response.content.strip()}

def translator_node(state:pipelineState)->dict:
    """step 3 : Translates the script into natural flowing Hinglish"""

    prompt = (
    "You are an expert content localizer for the Indian market. Take the following script "
    "and convert it into natural, flowing 'Hinglish'. Do not simply translate it sentence-by-sentence "
    "or repeat information. Alternating comfortably between Hindi and English phrases just as "
    "an intellectual tech educator would speak naturally on a live stream. Keep the energy "
    "and engagement intact. "
    "Return only the final Hinglish text.\n\n"
    f"Script:\n{state['script_text']}"
    )

    response=llm.invoke(prompt)

    return {"final_output":response.content.strip()}

#creating edges
from langgraph.graph import StateGraph, START, END

graph=StateGraph(pipelineState)  #defining state

#add nodes
graph.add_node("editor",editor_node)
graph.add_node("scriptwriter",scriptwriter_node)
graph.add_node("translator",translator_node)

#add edges( sequential - > one after other)
graph.add_edge(START,"editor")
graph.add_edge("editor","scriptwriter")
graph.add_edge("scriptwriter","translator")
graph.add_edge("translator",END)

#compile the graph
app=graph.compile()

result=app.invoke({
    "raw_input":"""Artificial intelligence is changing the way people learn and work.
Many companies are now using AI tools to automate repetitive tasks and improve productivity.
However, relying too much on artificial intelligence can reduce critical thinking and problem-solving skills.
It is important for students to understand how these technologies work rather than blindly depending on them.
The future will belong to people who can effectively combine human creativity with AI capabilities."""
})

#output
print("Final script",result["final_output"])
