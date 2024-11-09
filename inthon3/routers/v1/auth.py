import json
import base64
import datetime
import jwt
import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.leaf_models import User
from datetime import datetime, timedelta
import os
from pydantic import BaseModel
from jwt import algorithms

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"]
GOOGLE_KEYS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

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
    user = db.query(User).filter(User.oauth_id == oauth_id).first()
    if not user:
        print("신규 사용자입니다. 회원가입 처리")
        user = User(oauth_id=oauth_id, nickname="temp_user")
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
    # 헤더와 페이로드 추출 및 디코딩
    header, payload, _ = oi_token.split('.')
    header = json.loads(base64.urlsafe_b64decode(header + '=' * (4 - len(header) % 4)))
    payload = json.loads(base64.urlsafe_b64decode(payload + '=' * (4 - len(payload) % 4)))

    # 페이로드 유효성 검증
    if payload['iss'] not in GOOGLE_ISSUERS:
        raise HTTPException(status_code=400, detail="Invalid token issuer")
    if payload['exp'] < datetime.now().timestamp():
        raise HTTPException(status_code=400, detail="Token has expired")
    # if payload['aud'] != GOOGLE_CLIENT_ID:
    #     raise HTTPException(status_code=400, detail="Invalid token audience")

    # JWK (공개 키)로 서명 검증
    jwk_data = get_google_public_key(header['kid'])
    key = algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk_data))
    try:
        decoded = jwt.decode(oi_token, key=key, algorithms=['RS256'], audience=GOOGLE_CLIENT_ID)
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token signature")


def get_google_public_key(kid: str) -> dict:
    # Google의 공개 키를 가져와서 키 ID가 일치하는 키를 반환
    response = requests.get(GOOGLE_KEYS_URL)
    response.raise_for_status()
    keys = response.json().get("keys", [])
    for key in keys:
        if key["kid"] == kid:
            return key
    raise HTTPException(status_code=400, detail="Invalid token key ID")

# JWT 생성 함수
def create_jwt_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
