from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='sqlalchemy/login')

#secret_key
#algorithm
#expire

secret_key ='231dsad13a1sd23as1d5a6s41d32as1d32as1d65as41d0asdgfdgf12fg3132fs98af8sdf0as1'
algorithm = 'HS256'
expire_minutes = 30

# The tutorial makes a mistake here of not converting a datetime object into a string before jsonize it
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode["expiration"] = str(expire)
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# a "dependency" to check log-in authentication, this is in the path operation before a user can do a specific thing
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not vaidate credentials', 
    headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token()