
from fastapi import UploadFile, File, HTTPException
from utils import faces,files
from repositories import account_repo,face_repo
import os
import uuid
import configparser
from pyodbc import Row
from utils.faces import FindFace
import numpy as np
import cv2
import os
import warnings
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
import time
from elasticsearch import Elasticsearch, helpers
warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('example.ini')
es = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)


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
            elastic_response = faces.CreateEmbeding(image, acc.UserName, f'{acc.LastName} {acc.FirstName}' , image,customer_id)

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


#nhận diện khuôn mặt và lưu vào elastich search
def recognition(image, user):
    img_arr = read_image_cv2(image)
    
    #Xác minh thật giả
    spoofing  =  check_spoofing(img_arr)
    #Lấy thông tin nhận diện khuôn mặt trên elastic search
    face = FindFace(img_arr,user.CustomerID)

    #Nếu là người trên hệ thống ghi lại nhật ký nhận dạng vào elastic search\
    app_id  = user.CustomerID
    index = config['DEFAULT']['audit_index']
    index = index+"_"+ app_id if app_id else ''
    #Build object lưu nhật ký nhận dạng
    if face:
        #Lấy thông tin người dùng trong sqldb từ username trả về từ elastic search
        account =  account_repo.find_by_user_name(face.face_code)
        doc={
            
        }
        # response = es.index(index=index,document=doc)
    return {
        'spoofing':spoofing,
        'face':face
    }

def read_image_cv2(file: UploadFile) -> np.ndarray:
    npimg = np.frombuffer(file.file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img

#Kiểm tra xenm hình ảnh có đúng tỉ lệ chưu
def check_image(image):
    height, width, channel = image.shape
    if width/height != 3/4:
        print("Image is not appropriate!!!\nHeight/Width should be 4/3.")
        return False
    else:
        return True

#Kiểm tra là ảnh chứa khuôn mặt thật hay ảnh giả mạo    
def check_spoofing(image, model_dir="./resources/anti_spoof_models", device_id=0):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    result = check_image(image)
    if result is False:
        return
    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    # sum the prediction from single model's result
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))

    # draw result of prediction
    label = np.argmax(prediction)
    value = prediction[0][label]/2
    # if label == 1:
    #     result_text = "RealFace Score: {:.2f}".format(value)
    #     color = (255, 0, 0)
    # else:
    #     result_text = "FakeFace Score: {:.2f}".format(value)
    #     color = (0, 0, 255)
    # cv2.rectangle(
    #     image,
    #     (image_bbox[0], image_bbox[1]),
    #     (image_bbox[0] + image_bbox[2], image_bbox[1] + image_bbox[3]),
    #     color, 2)
    # cv2.putText(
    #     image,
    #     result_text,
    #     (image_bbox[0], image_bbox[1] - 5),
    #     cv2.FONT_HERSHEY_COMPLEX, 0.5*image.shape[0]/1024, color)

    # result_image_name = f'{time.time()}.jpg'
    # cv2.imwrite(result_image_name, image)
    return {
        'RealFace' : bool( label == 1),
        'Score':value
    }