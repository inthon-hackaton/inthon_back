from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db

class SampleRepository():
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db