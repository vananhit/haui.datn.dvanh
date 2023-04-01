
from repositories.dbcontext import cursor


# Lưu bản ghi vào sql sau khi thêm vào elastic search
def create_face(ID, _id, _index,Extension, AccountID,Type):
    sql = "INSERT INTO Faces(ID, _id, _index,Extension,AccountID,Type) VALUES(?,?,?,?,?,?)"
    cursor.execute(sql, ID, _id, _index,Extension, AccountID,Type)
    cursor.commit()
    return {
        'ID': ID,
        '_id': _id,
        '_index': _index,
        'Extension':Extension,
        'AccountID': AccountID,
        'Type':Type
    }

#Đếm số lượng khuôn mặt của account
def count_faces_by_account_id(account_id):
    sql = "SELECT COUNT(*) FROM Faces WHERE AccountID = ?"
    cursor.execute(sql,account_id)
    return cursor.fetchval()

#Tìm face theo id
def find_by_id(face_id):
    sql = "SELECT * FROM faces WHERE ID = ?"
    cursor.execute(sql, face_id)
    return cursor.fetchone()

def delete_by_id(face_id):
    sql = "DELETE FROM Faces WHERE ID=?"
    cursor.execute(sql,face_id)
    cursor.commit()

#Lấy dan sách các khuôn mặt của image
def get_face_list(account_id):
    sql = "SELECT * FROM Faces WHERE AccountID =?"
    cursor.execute(sql,account_id)
    return cursor.fetchall()