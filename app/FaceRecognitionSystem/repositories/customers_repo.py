from repositories.dbcontext import cursor

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