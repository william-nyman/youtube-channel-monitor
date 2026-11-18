import argparse
import logging
import pathlib

from . import monitor
from .cli import print_channels
from .storage import (
    create_channels_table,
    create_videos_table,
    delete_channel,
    get_channels,
    set_monitor_shorts,
    should_monitor_shorts,
)
from .youtube import get_youtube_channel, set_baseline_shorts

logger = logging.getLogger(__name__)


def main():
    pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

    create_channels_table()
    create_videos_table()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser(
        "add",
        help="Add a channel to monitor. Use the channels YouTube Handle as the second argument",
    )
    add_parser.add_argument("handle")

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a channel from monitoring. Use the channels channel_id as the second argument.",
    )
    delete_parser.add_argument("channel_id")

    shorts_parser = subparsers.add_parser(
        "shorts",
        help="Chose whether to monitor shorts videos. Use channel_id is second the argument and on or off as third argument. Monitor shorts is off by defualt.",
    )
    shorts_parser.add_argument("channel_id")
    shorts_parser.add_argument("setting", choices=["on", "off"])

    subparsers.add_parser("list", help="List monitored channels.")

    subparsers.add_parser("run", help="Start the channel monitor.")

    args = parser.parse_args()

    if args.command == "add":
        get_youtube_channel(args.handle)

    elif args.command == "delete":
        delete_channel(args.channel_id)

    elif args.command == "shorts":
        if args.setting == "on":
            if not should_monitor_shorts(args.channel_id):
                set_baseline_shorts(args.channel_id)
                set_monitor_shorts(args.channel_id, True)

        elif args.setting == "off":
            set_monitor_shorts(args.channel_id, False)

    elif args.command == "list":
        channels = get_channels()
        print_channels(channels)

    elif args.command == "run":
        monitor.main()


if __name__ == "__main__":
    main()
