import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException,Request
from pydantic import ValidationError
from models.CurrentUser import CurrentUser
SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def generate_token(payload:CurrentUser) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, 'payload':payload.dict()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
   
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        if payload.get('exp') < datetime.now().timestamp():
            raise HTTPException(status_code=403, detail="Token expired")
        
        
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )
#Lấy người dùng hiện tại
async def get_current_user(request: Request, http_authorization_credentials= Depends(reusable_oauth2))->CurrentUser:
    try:
        # Decode the JWT token and get user information
        decoded_token = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        request.state.user = decoded_token.get('payload')
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    # Return user information
    return request.state.user
