import argparse
import pathlib
import time

from .cli import print_channels
from .config import interval_minutes
from .storage import (
    create_channels_table,
    create_videos_table,
    delete_channel,
    get_channels,
)
from .youtube import check_for_new_video, get_youtube_channel


def main():
    pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

    create_channels_table()
    create_videos_table()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a channel to monitor. Use the channels YouTube Handle as second argument"
    )
    add_parser.add_argument("handle")

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a channel from monitoring. Use the channels channel_id as second argument."
    )
    delete_parser.add_argument("channel_id")

    subparsers.add_parser(
        "list",
        help="List monitored channels."
    )

    subparsers.add_parser(
        "run",
        help="Start the channel monitor."
    )

    args = parser.parse_args()

    if args.command == "add":
        get_youtube_channel(args.handle)

    elif args.command == "delete":
        delete_channel(args.channel_id)

    elif args.command == "list":
        channels = get_channels()
        print_channels(channels)


    elif args.command == "run":
        while True:
            check_for_new_video(get_channels())
            time.sleep(interval_minutes())


if __name__ == "__main__":
    main()
