import time, jwt
from typing import Dict 
from decouple import config 

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def signJWT(username: str):
    payload = {
        "username": username,
        "expires": time.time() + 300 #過期時間
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": token
    }
def signRefreshJWT(username: str):
    payload = {
        "username": username,
        "expires": time.time() +1209600 #過期時間
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "refresh_token": token
    }
    
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token 
        else: 
            return None 
    except:
        return {}