import logging
import re

import feedparser
import requests

from .exceptions import (
    ChannelNotFoundError,
)
from .models import Channel, Video

logger = logging.getLogger(__name__)


def check_if_short(link):
    return "/shorts/" in link


def resolve_channel_handle(handle):
    r = requests.get(f"https://www.youtube.com/{handle}")

    index = r.text.find('"mainEntity":')

    section = r.text[index - 50 : index + 1000]

    matches = re.search(
        r'.+mainEntity":{"@type":"Person","name":"(.+)","url":"https://www.youtube.com/channel/(UC[A-Za-z0-9_-]{22})"',
        section,
    )

    if matches:
        channel = Channel(
            channel_id=matches.group(2),
            name=matches.group(1),
        )
    else:
        raise ChannelNotFoundError

    return channel


def fetch_latest_video(channel):
    parsed = feedparser.parse(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel.channel_id}"
    )

    for video in parsed["entries"]:
        link = video["link"]

        if check_if_short(link):
            continue

        video = Video(
            yt_videoid=video["yt_videoid"],
            title=video["title"],
            link=video["link"],
            name=video["author"],
            published=video["published"],
            thumbnail=video["media_thumbnail"][0]["url"],
            channel_id=video["yt_channelid"],
        )

        return video


def fetch_latest_short(channel_id):
    parsed = feedparser.parse(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    )

    status = parsed.get("status")

    if status is not None and not 200 <= status < 300:
        logger.error(
            f"Feedparser request failed when fetching latest short, status code: HTTP {status}"
        )
        return

    if parsed.get("bozo"):
        bozo_exception = parsed.get("bozo_exception")
        logger.error(f"Feed problem: {bozo_exception}")

    for video in parsed["entries"]:
        link = video["link"]

        if check_if_short(link):
            video = Video(
                yt_videoid=video["yt_videoid"],
                title=video["title"],
                link=video["link"],
                name=video["author"],
                published=video["published"],
                thumbnail=video["media_thumbnail"][0]["url"],
                channel_id=video["yt_channelid"],
            )

            return video


def fetch_recent_videos(channel):
    parsed = feedparser.parse(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel.channel_id}"
    )

    status = parsed.get("status")

    if status is not None and not 200 <= status < 300:
        logger.error(
            f"Feedparser request failed for {channel.name} when fetching recent videos, status code: HTTP {status}"
        )
        return

    if parsed.get("bozo"):
        bozo_exception = parsed.get("bozo_exception")
        logger.error(f"Feed problem: {bozo_exception}")

    videos = []

    if not bool(channel.monitor_shorts):
        for video in parsed["entries"]:
            if not check_if_short(video["link"]):
                video = Video(
                    yt_videoid=video["yt_videoid"],
                    title=video["title"],
                    link=video["link"],
                    name=video["author"],
                    published=video["published"],
                    thumbnail=video["media_thumbnail"][0]["url"],
                    channel_id=video["yt_channelid"],
                )

                videos.append(video)

            if len(videos) == 5:
                break

    else:
        for video in parsed["entries"]:
            video = Video(
                yt_videoid=video["yt_videoid"],
                title=video["title"],
                link=video["link"],
                name=video["author"],
                published=video["published"],
                thumbnail=video["media_thumbnail"][0]["url"],
                channel_id=video["yt_channelid"],
            )

            videos.append(video)

            if len(videos) == 10:
                break

    return videos
