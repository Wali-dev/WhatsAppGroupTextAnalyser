from fastapi import APIRouter
from controllers.user_controller import router as user_controller_router

# Create main router for user-related endpoints
user_router = APIRouter()

# Include user controller routes
user_router.include_router(user_controller_router)