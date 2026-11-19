import asyncio
import pathlib
import threading

import uvicorn

from . import config, monitor, storage


def create_server():
    config = uvicorn.Config(
        "youtube_channel_monitor.api:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
    )
    server = uvicorn.Server(config)

    return server


async def run_server(server):
    await server.serve()
    print("Server has shut down.")


async def main():
    pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

    storage.create_channels_table()
    storage.create_videos_table()

    stop_event = threading.Event()

    monitor_thread = threading.Thread(
        target=monitor.run_monitor, args=(stop_event, config.interval_minutes())
    )

    monitor_thread.start()

    server = create_server()

    try:
        watch_monitor_task = asyncio.create_task(
            monitor.watch_monitor_status(monitor_thread, stop_event, server)
        )
        server_task = asyncio.create_task(run_server(server))

        await server_task
        stop_event.set()

        await watch_monitor_task

    finally:
        stop_event.set()
        monitor_thread.join()


if __name__ == "__main__":
    asyncio.run(main())
