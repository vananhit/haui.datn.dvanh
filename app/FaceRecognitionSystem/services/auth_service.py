from repositories import account_repo, customers_repo
from models.CurrentUser import CurrentUser
from typing import Optional


def verify_password(username, password) -> Optional[CurrentUser]:

    # Tìm tk trong bảng customers
    user = customers_repo.find_customer_by_username_and_password(
        username=username, password=password)

    if user:
        return CurrentUser(CustomerID=user.ID,
                           CustomerName=user.CustomerName,
                           UserName=user.MasterUserName,
                           Email=user.Email,
                           Phone=user.Phone,
                           Address=user.Address,
                           IsMasterAccount=True)

    # Tìm tk trong bảng accounts
    user = account_repo.find_account_by_username_and_password(
        username=username, password=password)

    if user:
        # kiển tra tk này thuộc customer nào
        cus = customers_repo.find_custommer_by_id(user.CustomerID)
        if cus:
           
            return CurrentUser(CustomerID=cus.ID,
                               CustomerName=cus.CustomerName,
                               AccountID=user.ID,
                               UserName=user.UserName,
                               Email=user.Email,
                               Phone=user.Phone,
                               FistName=user.FirstName,
                               LastName=user.LastName,
                               IsMasterAccount=False)
    return None
