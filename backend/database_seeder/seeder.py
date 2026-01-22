#!/usr/bin/env python3
"""
Database Seeder Script
This script seeds the database with initial data including a user account.
"""

from configs.database_config import db_config
from utils.password_utils import hash_password
from models.user_model import UserCreateModel, UserModel
from bson import ObjectId
import asyncio


def seed_database():
    """Seed the database with initial user data"""
    print("Starting database seeding...")
    
    # Get the database connection
    client = db_config.get_sync_client()
    db = client[db_config.database_name]
    
    # Define the user to be seeded
    user_email = "abc@domain.com"
    user_password = "123456abc"
    user_userid = "seeded_user_001"  # Unique identifier for the seeded user
    
    # Check if user already exists
    existing_user = db.users.find_one({"email": user_email})
    if existing_user:
        print(f"User with email {user_email} already exists. Skipping creation.")
        return
    
    # Hash the password
    hashed_password = hash_password(user_password)
    print(f"Password hashed successfully for user {user_email}")
    
    # Create the user document
    user_doc = {
        "userid": user_userid,
        "email": user_email,
        "password_hash": hashed_password
    }
    
    # Insert the user into the database
    result = db.users.insert_one(user_doc)
    
    if result.inserted_id:
        print(f"Successfully seeded user with email: {user_email}")
        print(f"User ID: {result.inserted_id}")
    else:
        print("Failed to seed user")
    
    # Close the database connection
    client.close()
    print("Database seeding completed.")


if __name__ == "__main__":
    seed_database()