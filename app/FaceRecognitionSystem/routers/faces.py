
from fastapi import APIRouter,Depends,UploadFile,File
from utils.security import validate_token,get_current_user
from models.CurrentUser import CurrentUser
from services import face_service
import numpy as np
from PIL import Image
import json
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

#Nhận diện khuôn mặt
@router.post('/faces/recognition',tags=['faces'], dependencies=[Depends(validate_token)])
def recognition(image:UploadFile = File(...), curent_user: dict =  Depends(get_current_user)):
    user = CurrentUser.parse_obj(curent_user)
    face = face_service.recognition(image, user)
    return face

#Lấy danh sách dữ liệu nhận dạng khuôn mặt của 1 người
@router.get('/faces',tags=['faces'],dependencies=[Depends(validate_token)])
def get_faces(account_id, current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    return face_service.get_face_list(account_id=account_id)
    