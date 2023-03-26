from pydantic import BaseModel

class AccountDto(BaseModel):
    CustomerID:str
    UserName:str
    Password:str
    Email:str
    FirstName:str
    LastName:str
    Address:str