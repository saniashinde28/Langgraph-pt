#so we are creating a graph
#first thing u create is state
import os

#1 ) typed dict
from typing import TypedDict
class State(TypedDict):
    topic:str
    summary:str
    score:int

#2) pydantic
#it is good at data validation and type checking at runtime
# Pydantic validates actual data at runtime and supports custom validation rules.
from pydantic import BaseModel,field_validator
class state(BaseModel):
    topic:str
    summary:str=""
    score:int

    #decorator
    @field_validator("score") #needs the variable name as an arguement
    @classmethod
    def score_positive(cls,v):
        #cls targets the main class, state class
        if v<0:
            raise ValueError("score must be positive")
        return v

#python data classes
#standard py dataclass but used very rarely
from dataclasses import dataclass,field
@dataclass
class State:
    topic:str=""
    summary:str=""
    score:int=0
    messages:list=field(default_factory=list) #Whenever a new State object is created, create a new empty list for its messages field.

from langgraph.graph import MessagesState

class State(MessagesState):
    #messages field is already included with add_messages reducer
    #just add your extra fields
    user_name:str
    language:str