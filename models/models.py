from pydantic import BaseModel, EmailStr, Field
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from bson import ObjectId


# Define allowed types of questions using an enum.
# Enums are good when you want to restrict values to a fixed set of options.
class QuestionType(str, Enum):
    YES_NO = "yes_no"
    SHORT_TEXT = "short_text"
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECTION = "multiple_selection"

# This represents a question that will be asked in a questionnaire.
# "options" is used for questions that need predefined choices.
class Question(BaseModel):
    question_id: str  # Unique ID for the question (used when storing answers)
    prompt: str       # The actual question text
    type: QuestionType
    options: Optional[List[str]] = None  # Only used for choice/selection types

# A simple user model.
class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
  # Maps MongoDB _id to id in Python
    name: str
    email: EmailStr  # Validated email field

# Event model includes basic info plus when it happens and what questions it asks.
class Event(BaseModel):
    id: Optional[str] = Field(alias="_id")  # This will be populated by MongoDB
    title: str
    description: Optional[str] = None
    created_by: str  # Refers to the User who created the event
    active: bool
    start_time: datetime  # When the event begins
    end_time: datetime    # When the event ends
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Auto-set timestamp
    questions: Optional[List[Question]] = None  # The questionnaire for this event

# Event Create model only for bost includes basic info plus when it happens and what questions it asks excludes creation time
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    created_by: str
    active: bool
    start_time: datetime
    end_time: datetime
    questions: Optional[List[Question]] = None

# Stores the record of someone attending an event.
# Includes their answers to the questionnaire.
class Attendance(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str     # Refers to the attending User
    event_id: str    # Refers to the Event being attended
    attended_at: datetime = Field(default_factory=datetime.utcnow)  # Auto-set time
    questionnaire_answers: Optional[Dict[str, Any]] = None
    # Answers are stored as a dictionary, e.g.:
    # { "q1": "yes", "q2": "Payments", "q3": ["Keynote", "Workshop"] }
