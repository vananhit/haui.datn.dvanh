import uuid
from  repositories.dbcontext import cursor
from dtos.auth.AccountDto import AccountDto
#Tìm tài khoản theo tên và mật khẩu
def find_account_by_username_and_password(username,password):
    sql = "SELECT * FROM Accounts WHERE UserName =? AND  Password =?"
    cursor.execute(sql,username,password)
    return cursor.fetchone()

#Tìm tài khoản theo username và email
def find_account_by_username_or_email(username,email):
    sql = "SELECT * FROM Accounts WHERE UserName=? OR Email=?"
    cursor.execute(sql,username,email)
    return cursor.fetchone()

#Thêm tài khoản
def insert_account(acc:AccountDto):
        sql="INSERT INTO Accounts(ID, UserName,Password,Email,FirstName,LastName,Address,CustomerID) VALUES(?,?,?,?,?,?,?,?)"
        param=(str(uuid.uuid4()),acc.UserName,acc.Password,acc.Email,acc.FirstName,acc.LastName,acc.Address,acc.CustomerID)
        cursor.execute(sql,param)
        cursor.commit()
        return param

    