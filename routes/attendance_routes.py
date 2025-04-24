from fastapi import APIRouter, HTTPException
from models.models import Attendance
from config.database import collection_attendance
from schemas.schema import list_attendances
from bson import ObjectId

attendance_router = APIRouter(prefix="/attendances", tags=["Attendance"])


# Create a new attendance record
@attendance_router.post("/")
async def create_attendance(attendance: Attendance):
    result = collection_attendance.insert_one(attendance.model_dump(by_alias=True))
    return {"message": "Attendance recorded", "id": str(result.inserted_id)}

# Get all attendance records
@attendance_router.get("/")
async def get_all_attendance():
    records = collection_attendance.find()
    return list_attendances(records)

# Get a single attendance record by its ID
@attendance_router.get("/{attendance_id}")
async def get_attendance_by_id(attendance_id: str):
    record = collection_attendance.find_one({"_id": ObjectId(attendance_id)})

    if not record:
        raise HTTPException(status_code=404, detail="Attendance not found")

    return list_attendances(record)

# Get attendance by event ID
@attendance_router.get("/event/{event_id}")
async def get_attendance_by_event(event_id: str):
    records = collection_attendance.find({"event_id": event_id})
    return list_attendances(records)

# Get attendance by user ID
@attendance_router.get("/user/{user_id}")
async def get_attendance_by_user(user_id: str):
    records = collection_attendance.find({"user_id": user_id})
    return list_attendances(records)

# Delete an attendance record by ID
@attendance_router.delete("/{attendance_id}")
async def delete_attendance(attendance_id: str):
    result = collection_attendance.delete_one({"_id": ObjectId(attendance_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return {"message": "Attendance deleted"}
