import pytest
from fastapi.testclient import TestClient

from youtube_channel_monitor import api, storage, youtube
from youtube_channel_monitor.api import app

client = TestClient(app)

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


def test_read_channels(saved_channel):
    response = client.get("/channels")
    assert response.status_code == 200
    assert response.json() == [{'channel_id': 'test_channel_id', 'name': 'Test Channel'}]


def test_create_channel(monkeypatch):
    monkeypatch.setattr(
        api,
        "get_youtube_channel",
        lambda handle: youtube.YoutubeChannel(
            channel_id="test_channel_id",
            name="Test Channel",
        )
    )
    response = client.post(
        "/channels",
        json={"handle": "@testchannel"},
    )

    assert response.status_code == 201
    assert response.json() == {'channel_id': 'test_channel_id', 'name': 'Test Channel'}


def test_delete_channel(saved_channel):
    response = client.delete("/channels/test_channel_id")

    assert storage.get_channels() == []
    assert response.status_code == 204
