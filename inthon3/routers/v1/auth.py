import json
import base64
import datetime
import jwt
import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import LeafUser
from datetime import datetime, timedelta
import os
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

JWT_SECRET_KEY = "leaf_jwt_secret"
#JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 3600

GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"]
GOOGLE_KEYS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_CLIENT_ID = "1067111695591-isu83qg3jtf69qlvabqj8ktafd3ngdje.apps.googleusercontent.com"
#GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class TokenRequest(BaseModel):
    oi_token: str

@router.post("/verify_token")
async def verify_token(request: TokenRequest, db: Session = Depends(get_db)):
    # oi token 검증
    oi_token = request.oi_token
    try:
        payload = validate_token(oi_token)
    except HTTPException as e:
        raise e

    # 검증된 토큰에서 유저 정보 추출
    oauth_id = payload['sub']

    # DB에서 사용자 조회 또는 신규 사용자 생성
    user = db.query(LeafUser).filter(LeafUser.oauth_id == oauth_id).first()
    if not user:
        print("신규 사용자입니다. 회원가입 처리")
        user = LeafUser(oauth_id=oauth_id, nickname="temp_user")
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        print("기존 사용자입니다. 로그인 처리")

    # JWT 발급
    access_token = create_jwt_token(user_id=user.user_id)

    return {
        "access_token": access_token,
    }

def validate_token(oi_token: str) -> dict:
    from jwt import PyJWKClient

    try:
        # PyJWKClient를 사용하여 키 가져오기
        jwks_client = PyJWKClient(GOOGLE_KEYS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(oi_token)

        # 토큰 디코딩 및 검증
        decoded = jwt.decode(
            oi_token,
            key=signing_key.key,
            algorithms=['RS256'],
            audience=GOOGLE_CLIENT_ID,
            issuer="https://accounts.google.com"
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token signature has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token signature: {str(e)}")

# JWT 생성 함수
def create_jwt_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
