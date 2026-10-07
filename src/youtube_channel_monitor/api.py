from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from .storage import get_channels
from .youtube import (
    ChannelAlreadyExistsError,
    ChannelNotFoundError,
    InvalidHandleError,
    get_youtube_channel,
)

app = FastAPI()

class YoutubeHandle(BaseModel):
    handle: str



@app.get("/")
def root():
    return {"message": "YouTube Channel Monitor API"}


@app.get("/channels")
def read_channels():
    return get_channels()


@app.post("/channels", status_code=status.HTTP_201_CREATED)
def create_channel(handle: YoutubeHandle):
    try:
        channel = get_youtube_channel(handle.handle)

    except ChannelNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )

    except InvalidHandleError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid handle"
        )

    except ChannelAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Channel already added"
        )

    return {
            "channel_id": channel.channel_id,
            "name": channel.name
    }
