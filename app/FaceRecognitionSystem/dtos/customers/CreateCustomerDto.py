from pydantic import BaseModel

class CreateCustomerDto(BaseModel):
    CustomerName:str
    Address:str
    Phone:str
    Email:str
    MasterUserName:str
    MasterPassword:str