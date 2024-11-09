inthon-back

- 폴더 설명
1. config -> db연결 처리하는 폴더
2. models -> db 테이블에 해당하는 class를 선언하는 폴더
3. repository -> db에 직접적으로 저장하는 폴더 및 작은 단위의 함수를 선언
4. routers -> api url를 선언하는 router 폴더 -> services에 있는 함수 하나와 연결하여 활용
5. services -> repository 폴더에 저장된 함수들을 가지고 하나의 서비스를 가진 함수를 선언하는 폴더
6. schemas -> 스키마를 저장하는 폴더
7. main.py -> 실질적으로 fastapi 서버를 구동하는 코드
