import pathlib

from . import monitor, storage


def main():
    pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

    storage.create_channels_table()
    storage.create_videos_table()

    monitor.main()


if __name__ == "__main__":
    main()
