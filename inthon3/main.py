from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from config.database import create_tables
from routers import routers_sample

# SWAGGER_HEADERS = {
#     "title": "",
#     "version": "v1", 
#     "description": "",
#     "contact": {
#         "name": "",
#         "url": "",
#     },
# }

create_tables()
app = FastAPI()

@app.get("/", status_code=200, include_in_schema=False)
async def root():
    return {"message": "FastAPI app is up and running!"}

app.include_router(routers_sample.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)