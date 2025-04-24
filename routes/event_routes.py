from fastapi import APIRouter, HTTPException
from models.models import Event, EventCreate
from config.database import collection_events
from schemas.schema import list_events
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events"])

# GET Request Methods
@router.get("/")
async def get_events():
    # Query all documents from the MongoDB events collection
    events = list_events(collection_events.find())
    
    # The list_events function transforms MongoDB documents into JSON-serializable dicts
    return events

@router.get("/{event_id}")
async def get_event(event_id: str):
    # Try to find the event by its _id in MongoDB
    event = collection_events.find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Reuse your existing serializer to format the result
    return list_events(event)

@router.get("/creator/{creator_id}")
async def get_events_by_creator(creator_id: str):
    # Find all events where created_by matches the user ID
    events = collection_events.find({"created_by": creator_id})

    # Use your existing serializer to format them
    return list_events(events)


# POST Request Method
@router.post("/")
async def post_event(event: Event):
    print(event)
    # Convert the Pydantic Event model to a MongoDB-compatible dictionary.
    # by_alias=True maps the 'id' field to '_id'.
    # exclude={"id"} ensures Pydantic doesn’t try to send id in the document you insert.
    # The _id will still be returned via result.inserted_id.
    result = collection_events.insert_one(event.model_dump(by_alias=True, exclude={"id"}))

    # Return a success message and the inserted event's ID
    return {"message": "Event created", "id": str(result.inserted_id)}

@router.post("/", response_model=Event)  # Defines a POST route at /events/ and returns a response in Event format
async def post_event(event: EventCreate):  # FastAPI automatically parses request body into an EventCreate model
    doc = event.model_dump()  # Convert the Pydantic model to a regular dictionary
    doc["created_at"] = datetime.utcnow()  # Add a server-side timestamp (not client-provided)

    result = collection_events.insert_one(doc)  # Insert the document into MongoDB and get the result (includes inserted_id)

    # Find the inserted document using the MongoDB-generated ID, and return it as an Event response model
    return Event(**collection_events.find_one({"_id": result.inserted_id}))


@router.put("/{event_id}")
async def update_event(event_id: str, updated_event: Event):
    # Try to update the document with _id = event_id
    result = collection_events.update_one(
        {"_id": ObjectId(event_id)},  # Convert string ID to MongoDB ObjectId
        {"$set": updated_event.model_dump(by_alias=True, exclude_unset=True)}  # Only update provided fields
        # exclude_unset=True ensures we only update the fields the user sent in (not overwrite with None).

    )

    # If no document was matched, the ID didn't exist
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event updated successfully"}

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    # Try to delete the event with this ID
    result = collection_events.delete_one({"_id": ObjectId(event_id)})

    # If nothing was deleted, the ID didn't match anything
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted successfully"}