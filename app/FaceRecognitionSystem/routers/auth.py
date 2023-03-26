from fastapi import APIRouter, Depends, HTTPException
from dtos.auth.LoginDto import LoginDto
from dtos.auth.AccountDto import AccountDto
from utils.security import generate_token, validate_token
from services import auth_service, account_service
router = APIRouter()


@router.post('/auth/login', tags=["auth"])
def login(user: LoginDto):
    verify = auth_service.verify_password(
        username=user.username, password=user.password, is_master_account=user.ismasteraccount)
    if verify:
        print(verify)
        return {
            'token': generate_token(payload=verify)
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post('/auth/account', tags=['auth'], dependencies=[Depends(validate_token)])
def create_account(acc: AccountDto):
    # Nếu tk chưa được tạo do validate thì báo lỗi 400
    ans = account_service.create_account(acc)
    if not ans:
        raise HTTPException(
            status_code=400,
            detail=f"Đầu vào không hợp lệ",
        )
    return ans
