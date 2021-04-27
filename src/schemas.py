from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime



class Songbase(BaseModel):
    name: str
    duration : int
    uploadTime: datetime


class Song(Songbase):
    class Config():
        orm_mode = True


class ShowSong(BaseModel):
    name: str
    duration: int
    uploadTime: datetime

    class Config():
        orm_mode = True


class PodcastBase(BaseModel):
    name: str
    duration: int
    uploadTime: datetime
    host: str
    participants : Optional[List[str]] = []


class Podcast(PodcastBase):
    class Config():
        orm_mode = True


class ShowPodcast(BaseModel):
    name: str
    duration: int
    uploadTime: datetime
    host: str
    participants : Optional[List[str]] = []

    class Config():
        orm_mode = True


class AudiobookBase(BaseModel):
    title: str
    author: str
    narrator: str
    duration: int
    uploadTime: datetime


class Audiobook(AudiobookBase):
    class Config():
        orm_mode = True

class ShowAudiobook(BaseModel):
    title: str
    author: str
    narrator: str
    duration: int
    uploadTime: datetime

    class Config():
        orm_mode = True

