
from fastapi import APIRouter,Depends,UploadFile,File
from utils.security import validate_token,get_current_user
from models.CurrentUser import CurrentUser
from services import face_service
from utils.faces import FindFace
import numpy as np
from PIL import Image
import cv2
from dtos.faces.CreateFace import CreateFace
def read_image_cv2(file: UploadFile) -> np.ndarray:
    npimg = np.frombuffer(file.file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img
router = APIRouter()

def read_image(file: UploadFile) -> np.ndarray:
    with Image.open(file.file) as img:
        img_arr = np.array(img)
    return img_arr

#Khách hàng hêm một khuôn mặt mới cho tài khoản vào db elastic search
@router.post('/faces',  tags=['faces'],dependencies=[Depends(validate_token)])
async def create_face( account_id:str , type:int ,image:UploadFile=File(...), current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
   
    return await face_service.create_face(account_id, user.CustomerID, image,type)
    
#Khách hàng xoá khuôn mặt cho tài khoản
@router.delete('/faces',tags=['faces'],dependencies=[Depends(validate_token)])
def delete_face(face_id, current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    face_service.delete_face(face_id,user.CustomerID)

@router.post('/faces/upload',tags=['faces'])
def upload(image:UploadFile = File(...)):
    img_arr = read_image_cv2(image)
    # do something with img_arr
    face = FindFace(img_arr,"081aeeaa-260a-4e49-9cd3-1274c942a720")
   
    return face
#Lấy danh sách dữ liệu nhận dạng khuôn mặt của 1 người
@router.get('/faces',tags=['faces'],dependencies=[Depends(validate_token)])
def get_faces(account_id, current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    return face_service.get_face_list(account_id=account_id)
    