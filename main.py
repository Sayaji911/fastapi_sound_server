from enum import Enum
from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src import models, schemas, database
from src.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


class AudioType(str, Enum):
    Song = "Song"
    Podcast = "Podcast"
    Audiobook = "Audiobook"


class EndpointSchema(BaseModel):
    song: Optional[schemas.Song]
    podcast: Optional[schemas.Podcast]
    audiobook: Optional[schemas.Audiobook]


@app.post("/{audio_type}", status_code=status.HTTP_200_OK)
def create(request_body: EndpointSchema, audio_type: AudioType, db: Session = Depends(database.get_db)):
    if audio_type == AudioType.Song:

        new_song = models.Song(name=request_body.song.name, duration=request_body.song.duration,
                               uploadTime=request_body.song.uploadTime)
        db.add(new_song)
        db.commit()
        db.refresh(new_song)
        return new_song
    elif audio_type == AudioType.Podcast:

        new_podcast = models.Podcast(name=request_body.podcast.name, duration=request_body.podcast.duration,
                                     uploadTime=request_body.podcast.uploadTime,
                                     host=request_body.podcast.host)
        db.add(new_podcast)
        db.commit()
        db.refresh(new_podcast)
        return new_podcast
    elif audio_type == AudioType.Audiobook:
        new_audiobook = models.Audiobook(title=request_body.audiobook.title, author=request_body.audiobook.author,
                                         narrator=request_body.audiobook.narrator,
                                         duration=request_body.audiobook.duration,
                                         uploadTime=request_body.audiobook.uploadTime)
        db.add(new_audiobook)
        db.commit()
        db.refresh(new_audiobook)
        return new_audiobook


@app.get('/{audio_type}')
def show_all(audio_type: AudioType, db: Session = Depends(database.get_db)):
    if audio_type == AudioType.Song:
        return db.query(getattr(models, audio_type)).all()
    elif audio_type == AudioType.Podcast:
        return db.query(getattr(models, audio_type)).all()
    elif audio_type == AudioType.Audiobook:
        return db.query(getattr(models, audio_type)).all()


@app.get('/{audio_type}/{audio_id}')
def show(audio_type: AudioType, audio_id: int, db: Session = Depends(database.get_db)):
    if audio_type == audio_type.Song:
        songs = db.query(models.Song).filter(models.Song.id == audio_id).first()
        if not songs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Song with id {audio_id} not found ')
        return songs
    elif audio_type == audio_type.Podcast:
        podcasts = db.query(models.Podcast).filter(models.Podcast.id == audio_id).first()
        if not podcasts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Podcast with id {audio_id} not found ')
        return podcasts
    elif audio_type == audio_type.Audiobook:
        audiobooks = db.query(models.Audiobook).filter(models.Audiobook.id == audio_id).first()
        if not audiobooks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Audiobook with id {audio_id} not found ')
        return audiobooks


@app.put('/{audio_type}}/{audio_id}')
def upload(audio_type: AudioType, request: EndpointSchema, audio_id: int, db: Session = Depends(database.get_db)):
    if audio_type == AudioType.Song:
        song_schema = request.song
        song_data = db.query(models.Song).filter(models.Song.id == audio_id).first()
        if not song_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with the id {audio_id} is not available")
        json_supplier = jsonable_encoder(song_data)
        update_data = song_schema.dict(exclude_unset=True)
        for field in json_supplier:
            if field in update_data != 0:
                setattr(song_data, field, update_data[field])
        db.commit()
        db.refresh(song_data)
        return song_data

    elif audio_type == AudioType.Podcast:
        podcast_schema = request.podcast
        podcast_data = db.query(models.Podcast).filter(models.Podcast.id == audio_id).first()
        if not podcast_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Podcast with the id {audio_id} is not available")
        json_supplier = jsonable_encoder(podcast_data)
        update_data = podcast_schema.dict(exclude_unset=True)

        for field in json_supplier:
            if field in update_data != 0:
                setattr(podcast_data, field, update_data[field])
        db.commit()
        db.refresh(podcast_data)
        return podcast_data
    elif audio_type == AudioType.Audiobook:
        audiobook_schema = request.audiobook
        audiobook_data = db.query(models.Audiobook).filter(models.Audiobook.id == audio_id).first()
        if not audiobook_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Audiobook with the id {audio_id} is not available")
        json_supplier = jsonable_encoder(audiobook_data)
        update_data = audiobook_schema.dict(exclude_unset=True)
        for field in json_supplier:
            if field in update_data != 0:
                setattr(audiobook_data, field, update_data[field])
        db.commit()
        db.refresh(audiobook_data)
        return audiobook_data


@app.delete("/{audio_type/{audio_id}}")
def destroy(audio_type: AudioType, audio_id: int, db: Session = Depends(database.get_db)):
    if audio_type == AudioType.Song:
        db.query(models.Song).filter(models.Song.id == audio_id).delete(synchronize_session=False)
        db.commit()
        return "Deleted Successfully"
    elif audio_type == AudioType.Podcast:
        db.query(models.Podcast).filter(models.Podcast.id == audio_id).delete(synchronize_session=False)
        db.commit()
        return "Deleted Succesfully"
    elif audio_type == AudioType.Song:
        db.query(models.Audiobook).filter(models.Audiobook.id == audio_id).delete(synchronize_session=False)
        db.commit()
        return "Deleted Successfully"
