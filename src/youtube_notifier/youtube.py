import re

import feedparser
import requests
from storage import save_channel_to_database


class YoutubeChannel:
    def __init__(self, channel_id: str, name: str):
        self.channel_id = channel_id
        self.name = name

    def save(self):
        save_channel_to_database(self.channel_id, self.name)


def get_youtube_channel_id_and_name():
    youtube_handle = input("What is the YouTube handle of the channel you want to track? ").strip()

    if re.search('^@[A-Za-z0-9](?:[A-Za-z0-9_.-]{1,28}[A-Za-z0-9])?$', youtube_handle):
        r = requests.get(f'https://www.youtube.com/{youtube_handle}')
        index = r.text.find('"mainEntity":')
        r = (r.text[index-50:index+1000])

        matches =  re.search(r'.+mainEntity":{"@type":"Person","name":"(.+)","url":"https://www.youtube.com/channel/(UC[A-Za-z0-9_-]{22})"', r)

        if matches:
            channel = YoutubeChannel(matches.group(2), matches.group(1))
            YoutubeChannel.save(channel)
    else:
        print("Invalid YouTube handle")


def check_for_new_video(channels):
    for channel in channels:
        parsed = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel["channel_id"]}')
        for video in parsed["entries"]:
            print(video["title"])
            print(video["yt_videoid"])
            print(video["published"])
