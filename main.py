from fastapi import FastAPI
from routes.event_routes import router as event_router
from routes.user_routes import router as user_router
from routes.attendance_routes import attendance_router

app = FastAPI()

app.include_router(event_router)
app.include_router(user_router)
app.include_router(attendance_router)
