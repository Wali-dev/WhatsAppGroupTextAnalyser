from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from middleware.auth_middleware import AuthMiddleware

from routes import router
from configs.database_config import db_config

app = FastAPI()

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    print("Connecting to MongoDB...")
    try:
        # Test the database connection
        database = await db_config.get_async_database()
        # Attempt to list collections to verify connection
        await database.list_collection_names()
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    print("Closing MongoDB connection...")
    # Close the client if needed
    # Note: In production, you might want to properly close the client here

@app.get("/")
def read_root():
    return {"Hello": "World"}