from pydantic import BaseModel
from typing import Optional
class Auth(BaseModel):
   isMaster:Optional[bool]