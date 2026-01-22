from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import jwt
from datetime import datetime, timedelta
from models.user_model import UserModel
from models.whatsapp_analysis_model import WhatsAppAnalysisDocument
from utils.password_utils import verify_password
from configs.database_config import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

# from pydantic import BaseModel, EmailStr




load_dotenv()

router = APIRouter(prefix="/user", tags=["user"])

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


# class LoginRequest(BaseModel):
#     userid: str
#     password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class LogoutResponse(BaseModel):
    message: str



@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
       
        user_doc = await db.users.find_one({"email": request.email})

        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user = UserModel(**user_doc)

       
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

     
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # print(user)

        access_token = create_access_token(
            data={
                "sub": str(user.userid),
                "email": user.email
            },
            expires_delta=access_token_expires
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """
    Logout user (client-side token removal)
    """
    return LogoutResponse(message="Successfully logged out")


class UserDataResponse(BaseModel):
    user_id: str
    analyses: List[WhatsAppAnalysisDocument]


@router.get("/data", response_model=UserDataResponse)
async def get_user_data(request: Request, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get all WhatsApp analysis data for the authenticated user
    """
    # Get user ID from request state (set by middleware)
    user_id = getattr(request.state, 'user_id', None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    try:
        # Find all WhatsApp analyses associated with this user
        cursor = db.whatsapp_analysis.find({"user_id": user_id})
        analyses = []

        async for doc in cursor:
            # Convert MongoDB _id to id field for Pydantic model
            doc["id"] = doc.pop("_id", None)
            analyses.append(WhatsAppAnalysisDocument(**doc))

        return UserDataResponse(user_id=user_id, analyses=analyses)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving user data: {str(e)}"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token containing the user ID
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt