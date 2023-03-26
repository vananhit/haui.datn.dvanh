import uuid
from repositories.dbcontext import cursor
from dtos.auth.AccountDto import AccountDto
import datetime

def find_account_by_username_and_password(username, password):
    sql = "SELECT * FROM Accounts WHERE UserName =? AND  Password =?"
    cursor.execute(sql, username, password)
    return cursor.fetchone()

# Tìm tài khoản theo username và email


def find_account_by_username_or_email(username, email):
    sql = "SELECT * FROM Accounts WHERE UserName=? OR Email=?"
    cursor.execute(sql, username, email)
    return cursor.fetchone()

# Thêm tài khoản
def insert_account(acc: AccountDto):
    sql = "INSERT INTO Accounts(ID, UserName,Password,Email,FirstName,LastName,Address,CustomerID, CreatedDate) VALUES(?,?,?,?,?,?,?,?,?)"
    param = (str(uuid.uuid4()), acc.UserName, acc.Password, acc.Email,
             acc.FirstName, acc.LastName, acc.Address, acc.CustomerID,datetime.datetime.now())
    cursor.execute(sql, param)
    cursor.commit()
    return param

#Lấy tất cả các tài khoản thuộc về khách hàng
def get_accounts_by_customer_id(customer_id,skip,take, search):
    sub_query = 'AND (UserName LIKE ? OR FirstName LIKE ? OR LastName LIKE ? OR Email LIKE ?)' if  search else ''
    sql = "SELECT * FROM Accounts WHERE CustomerID =? {searh} ORDER BY CreatedDate  OFFSET ? ROWS FETCH NEXT ? ROWS ONLY".format(searh= sub_query)
    count_sql= "SELECT COUNT(*) FROM Accounts WHERE CustomerID =? {searh}".format(searh= sub_query )
    q = f'%{search}%'
    ans={
        'data':[],
        'total':0
    }
    if not search:
        print(sql)
        cursor.execute(sql,customer_id,skip,take)
        ans['data'] = cursor.fetchall()
        cursor.execute(count_sql,customer_id)
        ans['total'] = cursor.fetchval()
    else:
        cursor.execute(sql,customer_id,q,q,q,q,skip,take)
        ans['data'] = cursor.fetchall()
        cursor.execute(count_sql,customer_id,q,q,q,q)
        ans['total'] = cursor.fetchval()
    return ans