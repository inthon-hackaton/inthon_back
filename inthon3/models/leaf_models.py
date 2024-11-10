from sqlalchemy import Column,String, Integer, Boolean, ForeignKey, Text, DateTime, PrimaryKeyConstraint, UUID
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class LeafUser(Base):
    __tablename__ = "leaf_user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    oauth_id = Column(String, unique = True)
    nickname = Column(String)
    description = Column(Text)
    picture_id = Column(UUID, ForeignKey("picture.picture_id"))


class Picture(Base):
    __tablename__ = "picture"

    picture_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    picture_link = Column(String(2048))

class Draft(Base):
    __tablename__ = "draft"

    draft_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(Text)
    created_at = Column(DateTime, default=current_timestamp())

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    picture_id = Column(UUID, ForeignKey("picture.picture_id"))


class Piece(Base):
    __tablename__ = "piece"

    piece_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    piece_number = Column(Integer)
    created_at = Column(DateTime, default=current_timestamp())
    description = Column(Text)

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    draft_id = Column(Integer, ForeignKey("draft.draft_id"))
    picture_id = Column(UUID, ForeignKey("picture.picture_id"))

class Completion(Base):
    __tablename__ = "completion"

    completion_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    created_at = Column(DateTime, default=current_timestamp())

class Includes(Base):
    __tablename__ = "includes"

    piece_id = Column(Integer, ForeignKey("piece.piece_id"))
    completion_id = Column(Integer, ForeignKey("completion.completion_id"))

    __table_args__ = (
        PrimaryKeyConstraint("piece_id", "completion_id"),
    )

class Likes(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("leaf_user.user_id"))
    piece_id = Column(Integer, ForeignKey("piece.piece_id"))

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "piece_id"),
    )


