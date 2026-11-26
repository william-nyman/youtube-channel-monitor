import re
import threading

from . import notifications, youtube_client
from .exceptions import (
    InvalidHandleError,
)
from .repositories import database
from .repositories.channel_repository import ChannelRepository
from .repositories.video_repository import VideoRepository


def validate_youtube_handle_format(handle):
    return re.search("^@[A-Za-z0-9](?:[A-Za-z0-9_.-]{1,28}[A-Za-z0-9])?$", handle)


def add_new_channel(handle):
    if not validate_youtube_handle_format(handle):
        raise InvalidHandleError

    channel = youtube_client.resolve_channel_handle(handle)

    video = youtube_client.fetch_latest_video(channel)

    if video is None:
        return

    print(video.title)

    with database.transaction() as connection:
        ChannelRepository(connection).save_channel(channel)
        VideoRepository(connection).save_video(video)

    return channel


def set_baseline_short(channel_id):
    video = youtube_client.fetch_latest_short(channel_id)

    if video is None:
        return

    print(video.title)

    with database.transaction() as connection:
        VideoRepository(connection).save_video(video)


def check_channel_for_new_videos(channel):
    videos = youtube_client.fetch_recent_videos(channel)

    if videos is None:
        return

    for video in reversed(videos):
        with database.transaction() as connection:
            video_exists = VideoRepository(connection).check_if_video_exist_in_database(
                video
            )

        if not video_exists and notifications.send_new_video_notification(video):
            with database.transaction() as connection:
                VideoRepository(connection).save_video(video)


def check_for_new_videos(channels):
    threads = []
    for channel in channels:
        t = threading.Thread(target=check_channel_for_new_videos, args=(channel,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
