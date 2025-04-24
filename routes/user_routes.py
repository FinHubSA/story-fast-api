from fastapi import APIRouter, HTTPException
from models.models import User
from config.database import collection_user
from bson import ObjectId
from schemas.schema import list_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(user: User):
    result = collection_user.insert_one(user.model_dump(by_alias=True, exclude_unset=True))
    return {"message": "User created", "id": str(result.inserted_id)}

@router.get("/")
async def get_users():
    users = collection_user.find()
    return list_users(users)

@router.get("/{user_id}")
async def get_user(user_id: str):
    user = collection_user.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return list_users(user)

@router.put("/{user_id}")
async def update_user(user_id: str, updated_user: User):
    result = collection_user.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user.model_dump(by_alias=True, exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = collection_user.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}