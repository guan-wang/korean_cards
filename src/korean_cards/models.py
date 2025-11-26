from pydantic import BaseModel, Field
from typing import List

class LearningItem(BaseModel):
    korean_phrase: str = Field(..., description="The word or grammar chunk.")
    components: List[str] = Field(..., description="Breakdown of roots/particles.")
    literal_meaning: str = Field(default="", description="Direct translation.")
    contextual_note: str = Field(default="", description="Why it is used here.")
    difficulty_level: str = Field(default="", description="Beginner, Intermediate, or Advanced.")

class Syllabus(BaseModel):
    items: List[LearningItem]

class DojoScenario(BaseModel):
    id: str = Field(..., description="Unique ID (e.g. 'scen_1').")
    title: str = Field(..., description="Short title (e.g. 'Coffee Shop').")
    scenario_description: str = Field(..., description="Full narrative setup.")
    user_role: str = Field(..., description="Who the user is.")
    required_tone: str = Field(..., description="Polite, Casual, etc.")
    target_items: List[str] = Field(..., description="Which phrases from the syllabus are practiced here.")

class ScenarioList(BaseModel):
    scenarios: List[DojoScenario]

# --- THE AGGREGATOR (For Unified Workflow) ---
class LessonPlan(BaseModel):
    """Holds both the Analysis and the Practice Scenarios"""
    syllabus: Syllabus
    practice_scenarios: ScenarioList

class EvaluationResult(BaseModel):
    is_correct: bool = Field(..., description="Did the user pass?")
    score: int = Field(..., description="Score 1-10.")
    feedback_text: str = Field(..., description="Coaching feedback.")
    better_alternative: str = Field(..., description="Native correction.")




