from  repositories.dbcontext import cursor

#Tìm tài khoản theo tên và mật khẩu
def find_customer_by_username_and_password(username,password):
    sql = "SELECT * FROM Accounts WHERE UserName =? AND  Password =?"
    cursor.execute(sql,username,password)
    return cursor.fetchone()