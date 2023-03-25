import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from typing import Union, Any
from fastapi import Depends, HTTPException
from pydantic import ValidationError
SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def generate_token(payload) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, 'payload':payload
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
   
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        if payload.get('exp') < datetime.now().timestamp():
            raise HTTPException(status_code=403, detail="Token expired")
        
        return payload.get('username')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

