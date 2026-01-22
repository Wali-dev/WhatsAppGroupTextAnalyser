from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
import jwt
import os
from configs.database_config import db_config
from models.user_model import UserModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = "HS256"


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.client = db_config.get_async_client()
    async def verify_token(self, token: str):
        """
        Verify the JWT Bearer token and return the user ID if valid
        """
        try:
            print(token)
            if token.startswith("Bearer "):
                token = token.split(" ", 1)[1]

            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )
            

            user_id = payload.get("sub")
            

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            db = self.client[db_config.database_name]
            user_doc = await db.users.find_one({"userid": user_id})

            if not user_doc:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User no longer exists",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return user_id

        except jwt.PyJWTError as e:
            print(f"JWT Error: {type(e).__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


    async def dispatch(self, request: Request, call_next):
        """
        Middleware to check for valid JWT token in Authorization header
        """
        # Skip authentication for certain routes (like health check, login, etc.)
        if request.url.path in ["/", "/health", "/api/v1/user/login", "/api/v1/user/register", "/user/login", "/user/register"] or \
           request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
            response = await call_next(request)
            return response

        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract token from header (format: "Bearer <token>")
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization scheme must be Bearer",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify the token
        user_id = await self.verify_token(token)

        # Add user info to request state for use in route handlers
        request.state.user_id = user_id

        response = await call_next(request)
        return response