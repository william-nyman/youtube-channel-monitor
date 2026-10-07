def print_channels(channels):
    print("Channels monitored:\n")
    print(f"{'NAME': <20} {'CHANNEL ID'}")
    print("_" * 50)

    for channel in channels:
        print(f"{channel['name']:<20} {channel['channel_id']}")
