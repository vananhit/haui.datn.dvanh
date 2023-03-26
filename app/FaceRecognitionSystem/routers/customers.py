
from fastapi import APIRouter,HTTPException,Depends
from dtos.customers.CreateCustomerDto import CreateCustomerDto
from services import customer_service
from utils.security import validate_token,get_current_user
from typing import Optional
from models.CurrentUser import CurrentUser
router = APIRouter()

#Tạp một khách hàng mới
@router.post("/customers/", tags=["customers"])
def create_customer(cus:CreateCustomerDto):
    ans  =customer_service.create_customer(cus)
    if not ans:
        raise HTTPException(
            status_code=400,
            detail='Đầu vào không hơp lệ'
        )
    return ans

#Lấy tất cá các tài khoản thuộc về khách hàng đó
@router.get("/customers/accounts",tags=['customers'], dependencies=[Depends(validate_token)])
def get_accounts(skip:int, take:int,search:Optional[str]=None, curent_user: dict =  Depends(get_current_user)):
    user = CurrentUser.parse_obj(curent_user)
    ans= customer_service.get_accounts_by_customer_id(user.CustomerID,skip,take,search)
    return ans

