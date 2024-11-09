import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # PyJWT 사용
from jwt import PyJWTError

# 환경변수에서 JWT 비밀 키 및 알고리즘 가져오기
#JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_KEY = "leaf_jwt_secret"
JWT_ALGORITHM = "HS256"

# HTTPBearer 인스턴스 생성 (토큰 추출)
bearer_scheme = HTTPBearer()

def decode_jwt(token: str):
    """JWT 토큰을 디코딩하고 유효성 검증"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Authorization 헤더에서 토큰 추출 후 검증, 유저 정보 반환"""
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": user_id}
