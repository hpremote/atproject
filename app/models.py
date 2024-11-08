from sqlalchemy import Column, String, UUID, ForeignKey, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
import enum
from .db import Base



class UserFiles(Base):
    __tablename__ = "user_files"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filetype = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    type = Column(Enum("image", "video", name="file_type"), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    # add user id 


class Messages(Base):
    __tablename__ = "messages"

    uuid = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    msg = Column(Text, nullable=True)
    sys_msg = Column(Text, nullable=True)
    file_id = Column(PG_UUID(as_uuid=True), ForeignKey('user_files.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    # add user id from which user or whom sent
