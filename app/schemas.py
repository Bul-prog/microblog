from typing import List, Optional
from pydantic import BaseModel

class ErrorOut(BaseModel):
    result: bool = False
    error_type: str
    error_message: str

class UserBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class UserShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserOut(UserBase):
    followers: List[UserShort] = []
    following: List[UserShort] = []

class MediaOut(BaseModel):
    id: int
    url: str
    class Config:
        orm_mode = True

class LikeOut(BaseModel):
    user_id: int
    name: str
    class Config:
        orm_mode = True

class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None

class TweetOut(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: UserBase
    likes: List[LikeOut]
    class Config:
        orm_mode = True

class FollowOut(BaseModel):
    result: bool = True


class GetUserResponse(BaseModel):
    result: bool
    user: UserOut
