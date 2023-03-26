
from fastapi import APIRouter,HTTPException
from dtos.customers.CreateCustomerDto import CreateCustomerDto
from services import customer_service

router = APIRouter()

#Tạp một khách hàng mới
@router.post("/customers/", tags=["customers"])
async def create_customer(cus:CreateCustomerDto):
    ans  =customer_service.create_customer(cus)
    if not ans:
        raise HTTPException(
            status_code=400,
            detail='Đầu vào không hơp lệ'
        )
    return ans


