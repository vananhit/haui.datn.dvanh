from repositories import account_repo, customers_repo


def verify_password(username, password, is_master_account):
    # nếu là tk master kiểm tra bảng customers ngược lại kiểm tra bảng accounts

    if is_master_account:
        user = customers_repo.find_customer_by_username_and_password(
            username=username, password=password)
        if user:
            return {
                'CustomerID': user.ID,
                'UserName': user.MasterUserName,
                'Email': user.Email,
                'Phone': user.Phone,
                'Address': user.Address,
                'Name': user.CustomerName,
                'IsMasterAccount': True
            }
    # Tìm tk trong bảng account
    user = account_repo.find_account_by_username_and_password(
        username=username, password=password)

    if user:
        # kiển tra tk này thuộc customer nào
        cus = customers_repo.find_custommer_by_id(user.CustomerID)
        if cus:
            return {
                'CustomerID': cus.ID,
                'AccountID': user.ID,
                'UserName': user.UserName,
                'Email': user.Email,
                'Phone': user.Phone,
                'FistName': user.FirstName,
                'LastName': user.LastName,
                'IsMasterAccount': False
            }
    return None
