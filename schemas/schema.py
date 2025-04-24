
# EVENTS SCHEMA
# This function handles how a single question inside an event is converted to a clean dictionary
def serialize_question(question) -> dict:
    return {
        "question_id": question["question_id"],     # Unique ID for the question
        "prompt": question["prompt"],               # The text of the question
        "type": question["type"],                   # The type (e.g., yes_no, short_text)
        "options": question.get("options")          # Optional list of answer choices, if applicable
        # .get() is used here to avoid KeyError if 'options' is not present
    }

# This function converts a single Event document (from MongoDB) to a serializable dictionary
def individual_event(event) -> dict:
    return {
        "id": str(event["_id"]),                        # Convert MongoDB ObjectId to string
        "title": event["title"],                        # Title of the event
        "description": event.get("description"),        # Optional field
        "created_by": str(event["created_by"]),         # Also an ObjectId that we convert to string
        "active": event["active"],                      # Boolean flag
        "start_time": event["start_time"].isoformat(),  # Format datetime to ISO string for JSON
        "end_time": event["end_time"].isoformat(),
        "created_at": event["created_at"].isoformat(),

        # This is a list comprehension.
        # It takes each question in the event's "questions" list,
        # applies the `serialize_question` function to it,
        # and creates a new list of serialized question dictionaries.
        # If "questions" is missing, it defaults to an empty list.
        "questions": [serialize_question(q) for q in event.get("questions", [])]
    }

# This function serializes a list of events.
# It's a list comprehension that applies `individual_event()` to each event in the input list.
def list_events(events) -> list:
    return [individual_event(event) for event in events]

#USER SCHEMA

def individual_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

def list_users(users) -> list:
    return [individual_user(user) for user in users]


#ATTENDANCE SCHEMA
def individual_attendance(att) -> dict:
    return {
        "id": str(att["_id"]),
        "user_id": str(att["user_id"]),
        "event_id": str(att["event_id"]),
        "attended_at": att["attended_at"].isoformat(),
        "questionnaire_answers": att.get("questionnaire_answers", {})
    }

def list_attendances(attendances) -> list:
    return [individual_attendance(att) for att in attendances]