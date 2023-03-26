from fastapi import APIRouter, Depends, HTTPException
from dtos.auth.LoginDto import LoginDto
from utils.security import generate_token,get_current_user
from services import auth_service
router = APIRouter()


@router.post('/auth/login', tags=["auth"])
def login(user: LoginDto):
    current_user = auth_service.verify_password(
        username=user.username, password=user.password)
    
    if current_user:
        return {
            'token': generate_token(payload=current_user)
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")



