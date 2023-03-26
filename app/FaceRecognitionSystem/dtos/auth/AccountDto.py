from pydantic import BaseModel

class AccountDto(BaseModel):
    UserName:str
    Password:str
    Email:str
    FirstName:str
    LastName:str
    Address:str