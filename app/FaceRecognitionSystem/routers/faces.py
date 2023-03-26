
from fastapi import APIRouter,Depends,UploadFile,File
from utils.security import validate_token,get_current_user
from models.CurrentUser import CurrentUser
from services import face_service
router = APIRouter()


#Khách hàng hêm một khuôn mặt mới cho tài khoản vào db elastic search
@router.post('/faces',  tags=['faces'],dependencies=[Depends(validate_token)])
async def create_face( account_id , file:UploadFile=File(...), current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    return await face_service.create_face(account_id, user.CustomerID, file)
    
#Khách hàng xoá khuôn mặt cho tài khoản
@router.delete('/faces',tags=['faces'],dependencies=[Depends(validate_token)])
def delete_face(face_id, current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    face_service.delete_face(face_id,user.CustomerID)