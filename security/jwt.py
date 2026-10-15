import jwt
from typing import Dict
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# encoding token
def encode_token(payload: Dict, secret: str, algo: str):
    return jwt.encode(payload, secret, algorithm=algo)

# checker for extracting and decoding token
def decode_token(token: str, secret: str, algo: str):
    # decode the token
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
        return payload 
    except jwt.exceptions.DecodeError:
        return "Error"



