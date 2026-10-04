from youtube_channel_monitor.config import interval_minutes


def test_interval_minutes(tmp_path, monkeypatch):
    config_file = tmp_path / "config.toml"
    config_file.write_text("check_interval_minutes = 5")

    monkeypatch.chdir(tmp_path)

    result = interval_minutes()

    assert result == 300
