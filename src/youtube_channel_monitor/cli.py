import argparse

from . import storage, youtube


def commands():
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

    args = parser.parse_args()

    if args.command == "add":
        youtube.get_youtube_channel(args.handle)

    elif args.command == "delete":
        storage.delete_channel(args.channel_id)

    elif args.command == "shorts":
        if args.setting == "on":
            if not storage.should_monitor_shorts(args.channel_id):
                youtube.set_baseline_shorts(args.channel_id)
                storage.set_monitor_shorts(args.channel_id, True)

        elif args.setting == "off":
            storage.set_monitor_shorts(args.channel_id, False)

    elif args.command == "list":
        channels = storage.get_channels()
        print_channels(channels)


def print_channels(channels):
    print("Channels monitored:\n")
    print(f"{'NAME': <20} {'CHANNEL ID': <30} {'MONITOR SHORTS'}")
    print("_" * 67)

    for channel in channels:
        shorts_status = "On" if channel["monitor_shorts"] else "Off"
        print(f"{channel['name']:<20} {channel['channel_id']:<30} {shorts_status}")
