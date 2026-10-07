import pytest

from youtube_channel_monitor import storage


@pytest.fixture
def db(tmp_path, monkeypatch):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(storage, "DB_PATH", test_database)

    storage.create_channels_table()
    storage.create_videos_table()


@pytest.fixture
def saved_channel(db):
    channel = {
        "channel_id": "test_channel_id",
        "name": "Test Channel",
    }

    storage.save_channel_to_database(
        channel["channel_id"],
        channel["name"],
    )

    return channel


@pytest.fixture
def saved_video(saved_channel):
    video = {
        "yt_videoid": "video123",
        "title": "Test Video",
        "link": "https://youtube.com/watch?v=video123",
        "author": "Test Channel",
        "published": "2026-10-05T12:00:00+00:00",
        "thumbnail": "https://example.com/thumbnail.jpg",
        "channel_id": saved_channel["channel_id"],
    }

    storage.add_video_to_database(
        video["yt_videoid"],
        video["title"],
        video["link"],
        video["author"],
        video["published"],
        video["thumbnail"],
        video["channel_id"],
    )

    return video


def get_all_videos():
    with storage.get_connection() as connection:
        return connection.execute(
            "SELECT * FROM videos"
        ).fetchall()


def test_save_channel_to_database(db):
    result = storage.save_channel_to_database(
        "test_channel_id",
        "Test Channel"
    )

    assert result is True

    channels = storage.get_channels()

    assert channels == [
        {
            "channel_id": "test_channel_id",
            "name": "Test Channel"
        }
    ]


def test_cannot_save_duplicate_channel(db):
    first_result = storage.save_channel_to_database(
        "test_channel_id",
        "Test Channel"
    )

    second_result = storage.save_channel_to_database(
        "test_channel_id",
        "Test Channel"
    )

    assert first_result is True
    assert second_result is False

    channels = storage.get_channels()

    assert len(channels) == 1


def test_delete_channel(saved_channel):
    storage.delete_channel(
        saved_channel["channel_id"]
    )

    channels = storage.get_channels()

    assert channels == []


def test_add_video_to_database(saved_channel):
    storage.add_video_to_database(
        "video123",
        "Test Video",
        "https://youtube.com/watch?v=video123",
        "Test Channel",
        "2026-10-05T12:00:00+00:00",
        "https://example.com/thumbnail.jpg",
        saved_channel["channel_id"]
    )

    videos = get_all_videos()

    assert len(videos) == 1
    assert videos[0]["yt_videoid"] == "video123"
    assert videos[0]["title"] == "Test Video"
    assert videos[0]["channel_id"] == saved_channel["channel_id"]


def test_cannot_add_duplicate_video(saved_video):
    storage.add_video_to_database(
        saved_video["yt_videoid"],
        saved_video["title"],
        saved_video["link"],
        saved_video["author"],
        saved_video["published"],
        saved_video["thumbnail"],
        saved_video["channel_id"],
    )

    videos = get_all_videos()

    assert len(videos) == 1


def test_delete_channel_deletes_videos_also(saved_video):
    storage.delete_channel(
        saved_video["channel_id"]
    )

    channels = storage.get_channels()
    videos = get_all_videos()

    assert channels == []
    assert len(videos) == 0


def test_check_if_video_exists(saved_video):
    result = storage.check_if_video_exist_in_database(
        saved_video["published"],
        saved_video["channel_id"]
    )

    assert result is True


def test_check_if_video_is_new(saved_video):
    result = storage.check_if_video_exist_in_database(
        "2026-10-05T13:00:00+00:00",
        saved_video["channel_id"]
    )

    assert result is False


def test_check_video_only_checks_given_channel(db):
    storage.save_channel_to_database(
        "channel_1",
        "Channel One"
    )

    storage.save_channel_to_database(
        "channel_2",
        "Channel Two"
    )

    storage.add_video_to_database(
        "video_1",
        "Video One",
        "https://youtube.com/watch?v=video_1",
        "Channel One",
        "2026-10-05T12:00:00+00:00",
        "thumbnail_1",
        "channel_1"
    )

    storage.add_video_to_database(
        "video_2",
        "Video Two",
        "https://youtube.com/watch?v=video_2",
        "Channel Two",
        "2026-10-05T20:00:00+00:00",
        "thumbnail_2",
        "channel_2"
    )

    result = storage.check_if_video_exist_in_database(
        "2026-10-05T13:00:00+00:00",
        "channel_1"
    )

    assert result is False


def test_video_is_new_when_channel_has_no_videos(saved_channel):
    result = storage.check_if_video_exist_in_database(
        "2026-10-05T12:00:00+00:00",
        saved_channel["channel_id"]
    )

    assert result is False
