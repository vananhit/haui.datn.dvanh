from repositories import customers_repo
from dtos.customers.CreateCustomerDto import CreateCustomerDto

#Tạo một khách hàng mới
def create_customer(cus:CreateCustomerDto):
    #Kiểm tra khách hàng đã tồn tại hay chưa
    if not customers_repo.find_customer_by_username_or_email__or_phone(cus.MasterUserName,cus.Email,cus.Phone):
        #Thêm khách hàng mới
        return customers_repo.create_customer(cus)
    return None
