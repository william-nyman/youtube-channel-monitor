from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import monitoring_service
from .exceptions import (
    ChannelAlreadyExistsError,
    ChannelNotFoundError,
    ChannelNotFoundInDatabaseError,
    InvalidHandleError,
)
from .repositories import database
from .repositories.channel_repository import ChannelRepository

app = FastAPI()

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")


class YoutubeHandle(BaseModel):
    handle: str


class ShortsSetting(BaseModel):
    monitor_shorts: bool


@app.get("/")
def root():
    return FileResponse("frontend/dist/index.html")


@app.get("/channels", status_code=status.HTTP_200_OK)
def read_channels():
    with database.transaction() as connection:
        channels = ChannelRepository(connection).get_channels()

    return channels


@app.post("/channels", status_code=status.HTTP_201_CREATED)
def create_channel(handle: YoutubeHandle):
    try:
        channel = monitoring_service.add_new_channel(handle.handle)

    except ChannelNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
        )

    except InvalidHandleError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid handle"
        )

    except ChannelAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Channel already added"
        )

    return {"channel_id": channel.channel_id, "name": channel.name}


@app.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: str):
    try:
        with database.transaction() as connection:
            ChannelRepository(connection).delete_channel(channel_id)

    except ChannelNotFoundInDatabaseError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Channel with ID "{channel_id}" was not found',
        )


@app.patch("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_shorts_setting(channel_id: str, setting: ShortsSetting):
    with database.transaction() as connection:
        should_monitor_shorts = ChannelRepository(connection).should_monitor_shorts(
            channel_id
        )

    if setting.monitor_shorts and not should_monitor_shorts:
        monitoring_service.set_baseline_short(channel_id)

    with database.transaction() as connection:
        ChannelRepository(connection).set_monitor_shorts(
            channel_id, setting.monitor_shorts
        )
