from repositories import customers_repo,account_repo
from dtos.auth.AccountDto import AccountDto 

#Thêm tk mới
def create_account(acc:AccountDto):
    #Kiểm tra tài khoản mới tạo thuộc về khách hàng nào
    if customers_repo.find_custommer_by_id(acc.CustomerID):
        #kiểm user name và email đã tồn tại chưa
        if not account_repo.find_account_by_username_or_email(username=acc.UserName,email=acc.Email):
            #Nếu chưa tồn tại email và username thì thêm tk mới
            return account_repo.insert_account(acc)
    return None
    