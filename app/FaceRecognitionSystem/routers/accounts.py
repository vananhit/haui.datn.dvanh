from fastapi import APIRouter, Depends, HTTPException
from dtos.auth.AccountDto import AccountDto
from utils.security import validate_token, get_current_user
from services import account_service
from models.CurrentUser import CurrentUser
router = APIRouter()

#Khách hàng tạo tài khoản người dùng
@router.post('/accounts/account', tags=['accounts'], dependencies=[Depends(validate_token)])
def create_account(acc: AccountDto, curent_user: dict = Depends(get_current_user)):
    user:CurrentUser = CurrentUser.parse_obj(curent_user)
    # Nếu tk không phải là tk master thì ko cho tạo 
    if not user.IsMasterAccount:
        raise HTTPException(
            status_code=403,
            detail="Chỉ có quản trị hệ thống  mới được tạo tài khoản"
        ) 
    #Kiểm tra xem tài khoản muốn tạo có trùng user_name và email với tk quản khách hàng 
    if acc.UserName == user.UserName or acc.Email == user.Email:
        return HTTPException(
            status_code=400,
            detail='Email hoặc UserName đã tồn tại!'
        )
    # Nếu tk chưa được tạo thì báo lỗi 400
    ans = account_service.create_account(
        acc.UserName, acc.Password, acc.Email, user.CustomerID, acc.FirstName, acc.LastName, acc.Address)
    if not ans:
        raise HTTPException(
            status_code=400,
            detail=f"Đầu vào không hợp lệ",
        )
    return ans
