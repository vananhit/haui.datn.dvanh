from repositories import customers_repo, account_repo
from dtos.customers.CreateCustomerDto import CreateCustomerDto
from pyodbc import Row

# Tạo một khách hàng mới


def create_customer(cus: CreateCustomerDto):
    # Kiểm tra khách hàng đã tồn tại hay chưa
    if not customers_repo.find_customer_by_username_or_email__or_phone(cus.MasterUserName, cus.Email, cus.Phone):
        # Thêm khách hàng mới
        return customers_repo.create_customer(cus)
    return None

# Lấy danh sách tài khoản thuộc về khách hàng
def get_accounts_by_customer_id(customer_id,skip,take,searh):
    ans = account_repo.get_accounts_by_customer_id(customer_id,skip,take,searh)
    if ans:
        ans['data']=[mapper(row) for row in ans['data']]
        return ans
    return []

#Chuyển đổi pydbc.Row sang object
def mapper(row: Row):
    ans={}
    for des in row.cursor_description:
        ans[des[0]]=row.__getattribute__(des[0])
    return ans
