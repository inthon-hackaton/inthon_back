from sqlalchemy import Column,String, Integer, Boolean, ForeignKey, Text, DateTime
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key = True, index = True)
    user_name = Column(String)