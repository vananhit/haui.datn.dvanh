from repositories.dbcontext import cursor
from dtos.customers.CreateCustomerDto import CreateCustomerDto
import uuid
import datetime
#Tìm khách hàng theo tên 
def find_customer_by_username_and_password(username,password):
    sql = "SELECT * FROM Customers WHERE MasterUserName =? AND  MasterPassword =?"
    cursor.execute(sql,username,password)
    return cursor.fetchone()

#Tìm customer theo mã tk
def find_custommer_by_id(customer_id):
    sql="SELECT * FROM Customers WHERE ID =?"
    cursor.execute(sql,customer_id)
    return cursor.fetchone()

#Tỉm khách hàng theo username, email, hoặc sdt
def find_customer_by_username_or_email__or_phone(username,email,phone):
    sql ="SELECT * FROM Customers WHERE MasterUserName=? OR Email =? OR Phone =?"
    cursor.execute(sql,username,email,phone)
    return cursor.fetchone()

#Tạo một khách hàng mới
def create_customer(cus:CreateCustomerDto):
    sql = "INSERT INTO Customers(ID,CustomerName,Address,Phone,Email,MasterUserName,MasterPassword,CreatedDate) VALUES(?,?,?,?,?,?,?,?)"
    param=(str(uuid.uuid4()), cus.CustomerName,cus.Address,cus.Phone,cus.Email,cus.MasterUserName,cus.MasterPassword,datetime.datetime.now())
    cursor.execute(sql,param)
    cursor.commit()
    return param


