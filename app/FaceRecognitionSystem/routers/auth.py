from fastapi import APIRouter, Depends, HTTPException
from dtos.auth.LoginDto import LoginDto
from utils.security import generate_token,get_current_user,validate_token
from services import auth_service
from models.CurrentUser import CurrentUser
from models.Auth import Auth
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

#xác minh người dùng
@router.post('/auth/authen',tags=["auth"],dependencies=[Depends(validate_token)])
def authen(item :Auth,current_user=Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
   
    if item.isMaster and not user.IsMasterAccount:
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )
    return user


