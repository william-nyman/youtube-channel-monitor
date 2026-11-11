import logging
import re
import threading

import feedparser
import requests

from .notifications import send_new_video_notification
from .storage import (
    add_video_to_database,
    check_if_video_exist_in_database,
    save_channel_to_database,
    should_monitor_shorts,
)

logger = logging.getLogger(__name__)


class InvalidHandleError(Exception):
    pass


class ChannelAlreadyExistsError(Exception):
    pass


class ChannelNotFoundError(Exception):
    pass


class YoutubeChannel:
    def __init__(self, channel_id: str, name: str):
        self.channel_id = channel_id
        self.name = name

    def save(self):
        return save_channel_to_database(self.channel_id, self.name)

    def set_baseline_video(self):
        parsed = feedparser.parse(
            f"https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}"
        )

        for video in parsed["entries"]:
            link = video["link"]

            if check_if_short(link):
                continue

            title = video["title"]
            name = video["author"]
            yt_videoid = video["yt_videoid"]
            published = video["published"]
            thumbnail = video["media_thumbnail"][0]["url"]
            channel_id = video["yt_channelid"]

            add_video_to_database(
                yt_videoid, title, link, name, published, thumbnail, channel_id
            )

            return

    @classmethod
    def extract_channel_id_and_name_from_handle(cls, handle: str):

        r = requests.get(f"https://www.youtube.com/{handle}")

        index = r.text.find('"mainEntity":')

        section = r.text[index - 50 : index + 1000]

        matches = re.search(
            r'.+mainEntity":{"@type":"Person","name":"(.+)","url":"https://www.youtube.com/channel/(UC[A-Za-z0-9_-]{22})"',
            section,
        )

        if matches:
            return cls(channel_id=matches.group(2), name=matches.group(1))


def get_youtube_channel(handle):

    if not re.search("^@[A-Za-z0-9](?:[A-Za-z0-9_.-]{1,28}[A-Za-z0-9])?$", handle):
        raise InvalidHandleError

    channel = YoutubeChannel.extract_channel_id_and_name_from_handle(handle)

    if channel is None:
        raise ChannelNotFoundError

    if not channel.save():
        raise ChannelAlreadyExistsError

    channel.set_baseline_video()
    return channel


def set_baseline_shorts(channel_id):
    parsed = feedparser.parse(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    )

    for video in parsed["entries"]:
        link = video["link"]

        if not check_if_short(link):
            continue

        title = video["title"]
        name = video["author"]
        yt_videoid = video["yt_videoid"]
        published = video["published"]
        thumbnail = video["media_thumbnail"][0]["url"]
        channel_id = video["yt_channelid"]

        add_video_to_database(
            yt_videoid, title, link, name, published, thumbnail, channel_id
        )

        return


def check_for_new_video(channels):
    def fetch_and_check_videos(channel):
        parsed = feedparser.parse(
            f"https://www.youtube.com/feeds/videos.xml?channel_id={channel['channel_id']}"
        )

        status = parsed.get("status")

        if status is not None and not 200 <= status < 300:
            logger.error(
                f"Feedparser request failed for {channel['name']}, status code: HTTP {status}"
            )
            return

        if parsed.get("bozo"):
            bozo_exception = parsed.get("bozo_exception")
            logger.error(f"Feed problem: {bozo_exception}")

        videos = []

        if not should_monitor_shorts(channel["channel_id"]):
            for video in parsed["entries"]:
                if not check_if_short(video["link"]):
                    videos.append(video)
                if len(videos) == 5:
                    break

        else:
            for video in parsed["entries"]:
                videos.append(video)
                if len(videos) == 10:
                    break

        for video in reversed(videos):
            published = video["published"]
            channel_id = video["yt_channelid"]
            yt_videoid = video["yt_videoid"]

            if not check_if_video_exist_in_database(published, channel_id, yt_videoid):
                link = video["link"]
                title = video["title"]
                name = video["author"]
                thumbnail = video["media_thumbnail"][0]["url"]

                if send_new_video_notification(title, thumbnail, name, published, link):
                    add_video_to_database(
                        yt_videoid, title, link, name, published, thumbnail, channel_id
                    )

    threads = []

    for channel in channels:
        t = threading.Thread(target=fetch_and_check_videos, args=(channel,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def check_if_short(link):
    return "/shorts/" in link
