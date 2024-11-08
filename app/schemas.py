from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    org: Optional[str]
    role: str = "user"


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    uuid: UUID4
    created_at: datetime
    modified_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserFileBase(BaseModel):
    filetype: str
    filename: str
    type: str
    description: Optional[str]
    url: str


class UserFileCreate(UserFileBase):
    pass


class UserFileResponse(UserFileBase):
    id: UUID4
    created_at: datetime
    modified_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    user_msg: Optional[str]
    system_msg: str
    file_id: Optional[UUID4]


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    uuid: UUID4
    created_at: datetime
    modified_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
