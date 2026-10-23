from unittest.mock import Mock

import pytest

from youtube_channel_monitor import youtube


def test_check_if_short_returns_true_for_short():
    result = youtube.check_if_short(
        "https://www.youtube.com/shorts/abc123"
    )

    assert result is True


def test_check_if_short_returns_false_for_normal_video():
    result = youtube.check_if_short(
        "https://www.youtube.com/watch?v=abc123"
    )

    assert result is False


def test_existing_video_is_not_added_to_database_or_notified(monkeypatch):
    fake_video = {
        "yt_videoid": "video123",
        "title": "Test Video",
        "link": "https://youtube.com/watch?v=video123",
        "author": "Test Channel",
        "published": "2026-10-05T12:00:00+00:00",
        "yt_channelid": "channel123",
        "media_thumbnail": [
            {"url": "https://example.com/thumbnail.jpg"}
        ],
    }

    fake_feed = {
        "entries": [fake_video]
    }

    monkeypatch.setattr(
        youtube.feedparser,
        "parse",
        lambda url: fake_feed
    )

    monkeypatch.setattr(
        youtube,
        "check_if_video_exist_in_database",
        lambda published, channel_id, yt_videoid: True
    )

    fake_add_video = Mock()
    fake_notification = Mock()

    monkeypatch.setattr(
        youtube,
        "add_video_to_database",
        fake_add_video
    )

    monkeypatch.setattr(
        youtube,
        "send_new_video_notification",
        fake_notification
    )

    channels = [
        {
            "channel_id": "channel123",
            "name": "Test Channel"
        }
    ]

    youtube.check_for_new_video(channels)

    fake_add_video.assert_not_called()
    fake_notification.assert_not_called()


def test_new_video_is_added_to_database_and_notified(monkeypatch):
    fake_video = {
        "yt_videoid": "video123",
        "title": "Test Video",
        "link": "https://youtube.com/watch?v=video123",
        "author": "Test Channel",
        "published": "2026-10-05T12:00:00+00:00",
        "yt_channelid": "channel123",
        "media_thumbnail": [
            {"url": "https://example.com/thumbnail.jpg"}
        ],
    }

    fake_feed = {
        "entries": [fake_video]
    }

    monkeypatch.setattr(
        youtube.feedparser,
        "parse",
        lambda url: fake_feed
    )

    monkeypatch.setattr(
        youtube,
        "check_if_video_exist_in_database",
        lambda published, channel_id, yt_videoid: False
    )

    fake_add_video = Mock()
    fake_notification = Mock()

    monkeypatch.setattr(
        youtube,
        "add_video_to_database",
        fake_add_video
    )

    monkeypatch.setattr(
        youtube,
        "send_new_video_notification",
        fake_notification
    )

    channels = [
        {
            "channel_id": "channel123",
            "name": "Test Channel"
        }
    ]

    youtube.check_for_new_video(channels)

    fake_add_video.assert_called_once()
    fake_notification.assert_called_once()


def test_check_if_short_ignores_shorts(monkeypatch):
    fake_video = {
        "yt_videoid": "video123",
        "title": "Test Video",
        "link": "https://youtube.com/shorts/video123",
        "author": "Test Channel",
        "published": "2026-10-05T12:00:00+00:00",
        "yt_channelid": "channel123",
        "media_thumbnail": [
            {"url": "https://example.com/thumbnail.jpg"}
        ],
    }

    fake_feed = {
        "entries": [fake_video]
    }

    monkeypatch.setattr(
        youtube.feedparser,
        "parse",
        lambda url: fake_feed
    )


    fake_check_if_video_exist_in_database = Mock()

    monkeypatch.setattr(
        youtube,
        "check_if_video_exist_in_database",
        fake_check_if_video_exist_in_database
    )

    channels = [
        {
            "channel_id": "channel123",
            "name": "Test Channel"
        }
    ]

    youtube.check_for_new_video(channels)

    fake_check_if_video_exist_in_database.assert_not_called()


def test_new_videos_are_added_oldest_first(monkeypatch):
    fake_feed = {
        "entries": [
            {
                "yt_videoid": "video_3",
                "title": "Video Three",
                "link": "https://youtube.com/watch?v=video_3",
                "author": "Test Channel",
                "published": "2026-10-06T15:00:00+00:00",
                "yt_channelid": "channel123",
                "media_thumbnail": [
                    {"url": "https://example.com/thumbnail_3.jpg"}
                ],
            },
            {
                "yt_videoid": "video_2",
                "title": "Video Two",
                "link": "https://youtube.com/watch?v=video_2",
                "author": "Test Channel",
                "published": "2026-10-06T14:00:00+00:00",
                "yt_channelid": "channel123",
                "media_thumbnail": [
                    {"url": "https://example.com/thumbnail_2.jpg"}
                ],
            },
            {
                "yt_videoid": "video_1",
                "title": "Video One",
                "link": "https://youtube.com/watch?v=video_1",
                "author": "Test Channel",
                "published": "2026-10-06T13:00:00+00:00",
                "yt_channelid": "channel123",
                "media_thumbnail": [
                    {"url": "https://example.com/thumbnail_1.jpg"}
                ],
            },
        ]
    }


    monkeypatch.setattr(
        youtube.feedparser,
        "parse",
        lambda url: fake_feed
    )

    monkeypatch.setattr(
        youtube,
        "check_if_video_exist_in_database",
        lambda published, channel_id, yt_videoid: False
    )

    fake_send_notification = Mock()

    monkeypatch.setattr(
        youtube,
        "send_new_video_notification",
        fake_send_notification
    )

    fake_add_video_to_database = Mock()

    monkeypatch.setattr(
        youtube,
        "add_video_to_database",
        fake_add_video_to_database
    )

    channels = [
        {
            "channel_id": "channel123",
            "name": "Test Channel"
        }
    ]

    youtube.check_for_new_video(channels)

    assert fake_add_video_to_database.call_count == 3

    first_call = fake_add_video_to_database.call_args_list[0]
    second_call = fake_add_video_to_database.call_args_list[1]
    third_call = fake_add_video_to_database.call_args_list[2]

    assert first_call.args[0] == "video_1"
    assert second_call.args[0] == "video_2"
    assert third_call.args[0] == "video_3"


def test_invalid_youtube_handle_raises_InvalidHandleError():
    with pytest.raises(youtube.InvalidHandleError):
        youtube.get_youtube_channel("@user name")

    with pytest.raises(youtube.InvalidHandleError):
            youtube.get_youtube_channel("ab")

    with pytest.raises(youtube.InvalidHandleError):
            youtube.get_youtube_channel("username.")

    with pytest.raises(youtube.InvalidHandleError):
            youtube.get_youtube_channel("@abcdefghijklmnopqrstuvwxyz12345")


def test_already_saved_channel_raises_ChannelAlreadyExistsError(monkeypatch):
    monkeypatch.setattr(
        youtube.YoutubeChannel,
        "save",
        lambda self: False
    )

    channel = youtube.YoutubeChannel("channel_123", "Test Channel")

    monkeypatch.setattr(
        youtube.YoutubeChannel,
        "extract_channel_id_and_name_from_handle",
        lambda handle: channel
    )

    with pytest.raises(youtube.ChannelAlreadyExistsError):
        youtube.get_youtube_channel("@test-handle")
