from unittest.mock import Mock

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
        lambda published, channel_id: True
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
        lambda published, channel_id: False
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
