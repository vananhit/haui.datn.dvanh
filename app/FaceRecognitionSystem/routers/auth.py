from fastapi import APIRouter, Depends,HTTPException
from dtos.auth.LoginDto import LoginDto
from dtos.auth.AccountDto import AccountDto
from utils.security import verify_password, generate_token,validate_token
from  services import auth_service
router = APIRouter()



@router.post('/auth',tags=["auth"])
def login(user: LoginDto):
    if verify_password(username=user.username, password=user.password):
        return {
            'token': generate_token()
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.post('/auth/account',tags=['auth'],dependencies=[Depends(validate_token)])
def create_account(acc:AccountDto):

    pass