from fastapi import UploadFile,Request
from typing import Annotated
from datetime import datetime, timedelta, date
import re
from collections import defaultdict
from configs.database_config import db_config
from models.whatsapp_analysis_model import WhatsAppAnalysisDocument, DayWiseStats
import os

async def parse_txt_controller(request: Request,file: Annotated[UploadFile, "The txt file to parse"]):
    content = await file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    
    # Regex pattern to parse each message line
    message_pattern = re.compile(
        r"(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s(?P<time>\d{1,2}:\d{2}(?:\s[AP]M)?)\s-\s(?P<user>[^:]+?):\s*(?P<message>.*)"
    )
    
    # Pattern to detect "added" messages
    join_pattern = re.compile(r"\badded\s+(?P<new_user>.+?)(?:\s*$)")
    
    daily_active_users = defaultdict(set)
    daily_new_users = defaultdict(set)
    user_active_days = defaultdict(set)
    all_dates = []
    
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
            
        msg_match = message_pattern.search(line)
        if not msg_match:
            continue
        
        date_str = msg_match.group("date")
        time_str = msg_match.group("time")
        user = msg_match.group("user").strip()
        message = msg_match.group("message").strip()
        
        # Parse date (handle both 2-digit and 4-digit years)
        try:
            if len(date_str.split('/')[-1]) == 4:
                date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()
            else:
                date_obj = datetime.strptime(date_str, "%m/%d/%y").date()
        except ValueError:
            continue
        
        all_dates.append(date_obj)
        
        # Track active user (exclude system messages)
        if not message.startswith("Messages and calls are end-to-end encrypted"):
            daily_active_users[date_obj].add(user)
            user_active_days[user].add(date_obj)
        
        # Check if this is an "added" message
        join_match = join_pattern.search(message)
        if join_match:
            new_user = join_match.group("new_user").strip()
            daily_new_users[date_obj].add(new_user)
    
    if not all_dates:
        return {"error": "No valid messages found"}
    
    latest_date = max(all_dates)
    start_date = latest_date - timedelta(days=6)
    
    day_wise_stats = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_wise_stats.append({
            "date": day.isoformat(),
            "new_users": len(daily_new_users.get(day, set())),
            "active_users": len(daily_active_users.get(day, set()))
        })
    
    # Find users active on 4+ days in the last 7 days
    active_4_days_users = [
        user for user, days in user_active_days.items()
        if len([d for d in days if start_date <= d <= latest_date]) >= 4
    ]
    
    # Prepare the result
    result = {
        "range": {
            "start": start_date.isoformat(),
            "end": latest_date.isoformat()
        },
        "day_wise_graph_data": day_wise_stats,
        "active_4_days_users": active_4_days_users
    }

    user_id = getattr(request.state, 'user_id', None)
    # Save to database
    try:
        # Convert day_wise_stats to proper format for the model
        day_wise_objects = [
            DayWiseStats(
                date=item["date"],
                new_users=item["new_users"],
                active_users=item["active_users"]
            ) for item in day_wise_stats
        ]

        # Create document to insert using the model
        analysis_doc = WhatsAppAnalysisDocument(
            filename=file.filename,
            upload_date=datetime.now(),
            range_start=start_date.isoformat(),
            range_end=latest_date.isoformat(),
            day_wise_graph_data=day_wise_objects,
            active_4_days_users=active_4_days_users,
            user_id=user_id
        )

        # Get database and collection
        database = await db_config.get_async_database()
        collection = database["whatsapp_analysis"]

        # Insert the document
        inserted_result = await collection.insert_one(analysis_doc.dict(exclude={"id": True}))

        # After save, return all the users data
        cursor = collection.find({"user_id": user_id})
        all_user_data = await cursor.to_list(length=None)
        
        # Convert ObjectId to string for JSON serialization
        for doc in all_user_data:
            doc["_id"] = str(doc["_id"])
            
        return {"user_id": user_id, "analyses":  all_user_data}

    except Exception as e:
        # Log the error but still return the analysis result
        print(f"Error saving to database: {str(e)}")
        result["database_error"] = str(e)
        return result