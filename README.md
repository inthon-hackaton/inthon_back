<div align="center">
<h2>[2024] InThon 💻</h2>
조각 그림 심리치료 프로젝트
</div>

## Index
  - [서비스 소개](#서비스-소개) 
  - [기능적 구현](#기능적-구현)
  - [팀원소개](#팀원-소개)
<!--  Other options to write Readme
  - [Deployment](#deployment)
  - [Used or Referenced Projects](Used-or-Referenced-Projects)
-->
## 서비스 소개
<!--Wirte one paragraph of project description -->  
### 배경
- 사회에서 자신의 역할과 자리를 찾지 못한 청년들이 많이 생김. 사회로부터 고립되고 큰 우울감을 느껴 스스로 생을 마감하는 청년들의 죽음으로 매년 청년 고독사 문제가 심각함
- 현대 사회에서 늘어나는 스트레스 지수에 비해 자신에게 집중하는 시간이 부족함
- 불안, 우울감, 불면증 등 심리적 어려움을 겪으면서도 대면 상담에 대한 부담감으로 인해 심리 상담을 쉽게 받지 못하는 경우가 많음

### 해결 방안 제안
- 어플을 활용하여 대면 상담의 부담을 줄이고, 참여형 미술치료를 제공
- 다양한 사람과의 협업을 통해서 미술 작품을 만들어서 자신감을 높이고 스트레스를 줄여줌
- 창의적인 작업을 하면서 '몰입' 상태에 들어가게 되고 스트레스를 잊고 스스로에게 집중하는 시간을 가지도록 함

## 기능적 구현
### 데이터베이스 연결
```
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Database connection successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
```
환경 변수에서 불러온 정보를 바탕으로, 데이터베이스에 연결되는 SQLAlchemy 엔진을 새성합니다. SessionLocal 객체를 만들어 데이터베이스 세션 관리를 지원합니다.

### 로그인/회원가입
```
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
```
- google oauth를 활용하여 구글 이메일을 통한 간편한 회원가입과 로그인을 제공합니다.
- 앱이 구글 인증 서버로부터 받은 oi token의 유효성을 검사하고 고유 id(oauth_id)를 추출해 사용자를 식별하고, JWT 기반 액세스 토큰을 앱에게 돌려줍니다.
### 메인 화면
- 사용자가 자신이 사용하고 싶은 밑그림을 선택
- 각 밑그림의 세부 사항을 확인
- 밑그림을 선택하면 다른 사람들이 그린 그 밑그림 위의 조각 그림들을 볼 수 있음
### 작품 업로드
- 사용자가 특정 밑그림을 선택하고, 거기서 어느 조각을 그릴지 골라, 자신이 그린 조각 그림을 사진으로 업로드하는 기능
### 작품 병합
- 전체 밑그림의 일부분인 자신의 조각 그림을 포함하여 다른 사람들의 조각을 모아 하나의 작품으로 만들고, 이를 공유 및 저장하는 기능
### 마이 페이지
- 자신이 올린 조각 그림 수, 받은 좋아요 수, 나의 조각이 다른 사람의 작품에 사용된 횟수를 볼 수 있는 화면

## 팀원 소개

| 팀원 | 역할 | 소개 |
|------|------|------|
| ![민준](https://example.com/photo2.png) | **김민준** | 모바일 앱 개발 |
| ![다영](https://example.com/photo1.png) | **최다영** | 모바일 앱 개발 |
| ![의찬](https://example.com/photo3.png) | **박의찬** | 백엔드 개발 |
| ![준희](https://example.com/photo3.png) | **한준희** | 백엔드 개발 |
