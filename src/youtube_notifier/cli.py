

def print_channels(rows):
    print("Channels monitored:\n")
    print(f"{'NAME': <20} {'CHANNEL ID'}")
    print("_" * 50)

    for channel in rows:
        print(f"{channel['name']:<20} {channel['channel_id']}")
