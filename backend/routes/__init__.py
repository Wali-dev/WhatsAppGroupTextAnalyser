from fastapi import APIRouter, File, UploadFile, Depends, Request
from controllers.message_controller import parse_txt_controller
from validation.file_validator import validate_txt_file
from routes.user_routes import user_router

router = APIRouter(prefix="/api/v1")

# Include user routes under /api/v1/user
router.include_router(user_router)

@router.get("/health")
def health_check():
    return {"status": "healthy"}

def validated_file(file: UploadFile = File(...)):
    return validate_txt_file(file)

def require_authentication(request: Request):
    """Dependency to ensure user is authenticated"""
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user_id

@router.post("/parse-txt")
async def parse_txt_endpoint(request: Request, file: UploadFile = Depends(validated_file)):
    return await parse_txt_controller(request, file)