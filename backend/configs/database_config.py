from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional


class DatabaseConfig:
    """
    Configuration class for MongoDB connection
    """

    def __init__(self):
        # Get MongoDB connection details from environment variables or use defaults
        mongodb_base_url = "mongodb+srv://cornell:demopass123@cluster0.vvkfg79.mongodb.net/whatsapp_text_analyzer"
        self.mongodb_url = os.getenv("MONGODB_URL", mongodb_base_url)
        self.database_name = os.getenv("DATABASE_NAME", "whatsapp_text_analyzer")
        
    def get_sync_client(self) -> MongoClient:
        """Get synchronous MongoDB client"""
        return MongoClient(self.mongodb_url, tls=True)

    def get_async_client(self) -> AsyncIOMotorClient:
        """Get asynchronous MongoDB client for async operations"""
        return AsyncIOMotorClient(self.mongodb_url, tls=True)
    
    def get_database(self):
        """Get database instance"""
        client = self.get_sync_client()
        return client[self.database_name]
    
    async def get_async_database(self):
        """Get async database instance"""
        client = self.get_async_client()
        return client[self.database_name]


# Global instance
db_config = DatabaseConfig()


async def get_database():
    """Dependency function for FastAPI to get database instance"""
    return await db_config.get_async_database()