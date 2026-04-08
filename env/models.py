from pydantic import BaseModel
from typing import Dict

class Observation(BaseModel):
    code: str
    language: str
    step: str

class Action(BaseModel):
    issue: str
    impact: str
    fix: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict