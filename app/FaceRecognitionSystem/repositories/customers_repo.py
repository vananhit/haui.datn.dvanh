from dbcontext import cursor

#Tìm khách hàng theo tên 
def find_customer_by_username_and_password(name,value):
    sql = "SELECT * FROM Customers WHERE MasterUserName = "