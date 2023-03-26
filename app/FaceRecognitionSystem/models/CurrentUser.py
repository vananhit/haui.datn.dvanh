from pydantic import BaseModel
from typing import Optional
class CurrentUser(BaseModel):
    CustomerID:str
    CustomerName:str
    AccountID:Optional[str]
    UserName:str
    Email:str
    Phone:str
    Address:Optional[str]
    FistName:Optional[str]            
    LastName:Optional[str]
    IsMasterAccount :str    