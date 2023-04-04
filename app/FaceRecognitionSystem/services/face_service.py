
from fastapi import UploadFile, File, HTTPException
from utils import faces,files
from repositories import account_repo,face_repo
import os
import uuid
import configparser
from pyodbc import Row
config = configparser.ConfigParser()
config.read('example.ini')

#Tạo khuôn mặt cho tài khoản
async def create_face(account_id, customer_id, file: UploadFile = File(...), type=1):
    
    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=400,
            detail='File tải lên không phải là ảnh!'
        )
    # Check xem account có tồn tại và thuộc về khách hàng
    acc = account_repo.find_by_id(account_id)
    if acc and acc.CustomerID == customer_id:

        #Kiểm tra xem account đó đã lấy đủ 3 ảnh hay chưa nếu đủ rồi thì không cho thêm
        total_face= face_repo.count_faces_by_account_id(account_id)
        if total_face>=8:
            raise HTTPException(status_code=400,detail='Tài khoản này đã có đủ 8 khuôn mặt')

        # Lưu file vào ổ đĩa cứng
        # Tạo một thư mục để lưu file nếu chưa tồn tại
        if not os.path.exists(f'uploads/{customer_id}/{account_id}'):
            os.makedirs(f'uploads/{customer_id}/{account_id}')

        # Lưu file vào thư mục uploads trên server
        face_id = str(uuid.uuid4())
        file_name = f'{face_id}.{file.filename.split(".")[-1]}'

        with open(os.path.join(f'uploads/{customer_id}/{account_id}', file_name), "wb") as buffer:
            buffer.write(await file.read())

        image = f'./uploads/{customer_id}/{account_id}/{file_name}'
       
       
        
        try:
            # thêm khuôn mặt vào elastic searh
            elastic_response = faces.CreateEmbeding(image, acc.UserName, image,customer_id)

            # lấy id và index do elastic search trả về và lưu vào sql
            extension =f'.{file.filename.split(".")[-1]}'
            return face_repo.create_face(face_id,elastic_response.get('_id'),elastic_response.get('_index'),extension,acc.ID,type)

        except Exception as e:
            print(e)
            #Xoá ảnh vừa upload lên nếu việc lưu vào elastic search vả sql bị lỗi
            files.delete_file_if_exists(image)
            raise HTTPException(
                status_code=500,
                detail='Thêm khuôn mặt bị lỗi'
            )
    else:
        raise HTTPException(
            status_code=400,
            detail='Tài khoản không tồn tại!'
        )
        
    
#Xoá khuôn mặt cho tài khoản
def delete_face(face_id,customer_id):
    #kiểm tra xem face_id có thuộc quyền quản lý của customer
    face = face_repo.find_by_id(face_id)
    #nếu tồn tại khuôn mặt tìm account và kiểm tra customer id có quản lý face này hay không
    if face:
        #Tìm account
        acc = account_repo.find_by_id(face.AccountID)
        #kiểm tra xem customer_id có trùng hay không
        if acc.CustomerID == customer_id:
            try:
                #Xoá khuôn mặt trên elastic search
                faces.DeleteEmbeding(index_name=face._index, doc_id=face._id)
                #Xoá khuôn mặt trên sql
                face_repo.delete_by_id(face.ID)
                #Xoá khuôn mặt trong file uploads
                image = f'./uploads/{customer_id}/{acc.ID}{face.Extension}'
                files.delete_file_if_exists(image)
                return True
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=500,
                    detail='Có lỗi xẩy ra vui lòng liên hệ quản trị hệ thống để được giúp đỡ!'
                )
    raise HTTPException(
        status_code=400,
        detail='Đầu vào không hợp lệ!'
    )    
 #Lấy danh sách các dữ liệu nhận dạng của 1 tài khoản      
def get_face_list(account_id):
    data =  face_repo.get_face_list(account_id=account_id)
    if data :
            return [mapper(row) for row in data]
    
    return []

#Chuyển đổi pydbc.Row sang object
def mapper(row: Row):
    ans={}
    for des in row.cursor_description:
        ans[des[0]]=row.__getattribute__(des[0])
    return ans
