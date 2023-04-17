from fastapi import APIRouter,Depends,UploadFile,File
from utils.security import validate_token,get_current_user
from models.CurrentUser import CurrentUser
from services import recognition_history_service as appService
router = APIRouter()

@router.get('/recognition-history',tags=['recognition-history'],dependencies=[Depends(validate_token)])
def getAuditLog(skip, take,  fromDate, toDate, search =None,current_user:dict = Depends(get_current_user)):
    user = CurrentUser.parse_obj(current_user)
    return appService.getAuditLog(skip,take,fromDate,toDate,search, user)