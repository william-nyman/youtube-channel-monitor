def print_channels(channels):
    print("Channels monitored:\n")
    print(f"{'NAME': <20} {'CHANNEL ID': <30} {'MONITOR SHORTS'}")
    print("_" * 67)

    for channel in channels:
        shorts_status = "On" if channel["monitor_shorts"] else "Off"
        print(f"{channel['name']:<20} {channel['channel_id']:<30} {shorts_status}")
