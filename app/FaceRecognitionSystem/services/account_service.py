from repositories import customers_repo,account_repo
from dtos.auth.AccountDto import AccountDto 

#Thêm tk mới
def create_account(user_name, password, email, customer_id, first_name, last_name, address):

    #kiểm user name và email đã tồn tại chưa
    if not account_repo.find_account_by_username_or_email(username=user_name,email=email):
        #Nếu chưa tồn tại email và username thì thêm tk mới
        return account_repo.insert_account(user_name, password, email, customer_id, first_name, last_name, address)
        
    return None
    
