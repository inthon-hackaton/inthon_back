from sqlalchemy import Column,String, Integer, Boolean, ForeignKey, Text, DateTime, URL
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base

class Leaf_User(Base):
    __tablename__ = "leaf_user"

    user_id = Column(Integer, primary_key = True, index = True)
    nickname = Column(String, unique = True)

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index = True)
    pw = Column(String)
    email = Column(String)
    name = Column(String)
    description = Column(Text)

    leaf_user_id = Column(Integer, ForeignKey("leaf_user.user_id"))

class Picture(Base):
    __tablename__ = "picture"

    picture_id = Column(Integer, primary_key=True, index=True)
    picture_link = Column(URL)

class Draft(Base):
    __tablename__ = "draft"

    draft_id = Column(Integer, primary_key= True, index = True)
    description = Column(Text)
    created_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    picture_id = Column(Integer, ForeignKey("picture.picture_id"))

class Piece(Base):
    piece_id = Column(Integer, primary_key=True, index=True)
    piece_number = Column(Integer)
    created_at = Column(DateTime)
    description = Column(Text)

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    draft_id = Column(Integer, ForeignKey("draft.draft_id"))
    picture_id = Column(Integer, ForeignKey("picture.picture_id"))

class Completion(Base):
    completion_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    picture_id = Column(Integer, ForeignKey("picture.picture_id"))

class Includes(Base):
    piece_id = Column(Integer, ForeignKey("piece.piece_id"))
    completion_id = Column(Integer, ForeignKey("completion.completion_id"))

class Likes(Base):
    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    piece_id = Column(Integer, ForeignKey("piece.piece_id"))

