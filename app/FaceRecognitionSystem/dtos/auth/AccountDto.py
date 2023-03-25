from pydantic import BaseModel

class AccountDto(BaseModel):
    ID:str
    UserName:str
    FirstName:str
    LastName:str