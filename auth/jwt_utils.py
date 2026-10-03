from jose import jwt 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECREAT_KEY = os.environ.get("SECREAT_KEY", "helloworld")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECREAT_KEY, algorithm=ALGORITHM)

def decode_access_token(token:str) -> dict:
    return jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])



    

