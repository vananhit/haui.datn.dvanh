from pydantic import BaseModel
from fastapi import UploadFile,File
class CreateFace(BaseModel):
    account_id:str
    face_type:int
    image:UploadFile = File(...)