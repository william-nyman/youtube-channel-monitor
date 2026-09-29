import re

import feedparser
import requests
from notifications import send_new_video_notification
from storage import (
    add_video_to_database,
    check_if_video_exist_in_database,
    save_channel_to_database,
)


class YoutubeChannel:
    def __init__(self, channel_id: str, name: str):
        self.channel_id = channel_id
        self.name = name

    def save(self):
        save_channel_to_database(self.channel_id, self.name)

    def set_baseline_video(self):
        parsed = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}')

        video = parsed["entries"][0]

        yt_videoid = video["yt_videoid"]
        title = video["title"]
        link = video["link"]
        name = video["author"]
        published = video["published"]
        thumbnail = video["media_thumbnail"][0]["url"]
        channel_id = video["yt_channelid"]

        add_video_to_database(yt_videoid, title, link, name, published, thumbnail, channel_id)
        send_new_video_notification(title, thumbnail, name, published, link)

    @classmethod
    def extract_channel_id_and_name_from_handle(cls, handle: str):
        if re.search('^@[A-Za-z0-9](?:[A-Za-z0-9_.-]{1,28}[A-Za-z0-9])?$', handle):

            r = requests.get(f'https://www.youtube.com/{handle}')

            index = r.text.find('"mainEntity":')

            section = (r.text[index-50:index+1000])

            matches =  re.search(r'.+mainEntity":{"@type":"Person","name":"(.+)","url":"https://www.youtube.com/channel/(UC[A-Za-z0-9_-]{22})"', section)

            if matches:
                return cls(
                    channel_id = matches.group(2),
                    name = matches.group(1)
                )
        else:
            print("Invalid YouTube handle")



def get_youtube_channel():
    handle = input("What is the YouTube handle of the channel you want to track? ").strip()

    channel = YoutubeChannel.extract_channel_id_and_name_from_handle(handle)

    if channel is not None:
        channel.save()
        channel.set_baseline_video()


def check_for_new_video(channels):
    for channel in channels:
        parsed = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel["channel_id"]}')

        for video in reversed(parsed["entries"][:3]):
            published = video["published"]
            channel_id = video["yt_channelid"]

            if not check_if_video_exist_in_database(published, channel_id):
                yt_videoid = video["yt_videoid"]
                title = video["title"]
                link = video["link"]
                name = video["author"]
                published = video["published"]
                thumbnail = video["media_content"]["media_thumbnail"][0]["url"]
                channel_id = video["yt_channelid"]

                add_video_to_database(yt_videoid, title, link, name, published, thumbnail, channel_id)

                send_new_video_notification(title, thumbnail, name, published, link)
