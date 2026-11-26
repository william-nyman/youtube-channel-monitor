import asyncio
import pathlib
import threading

import uvicorn

from youtube_channel_monitor import monitoring_worker
from youtube_channel_monitor.repositories.video_repository import VideoRepository

from . import config
from .repositories import database
from .repositories.channel_repository import ChannelRepository


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

    with database.transaction() as connection:
        ChannelRepository(connection).create_channel_table()
        VideoRepository(connection).create_videos_table()

    stop_event = threading.Event()

    monitor_thread = threading.Thread(
        target=monitoring_worker.run_monitor,
        args=(stop_event, config.interval_minutes()),
    )

    monitor_thread.start()

    server = create_server()

    try:
        watch_monitor_task = asyncio.create_task(
            monitoring_worker.watch_monitor_status(monitor_thread, stop_event, server)
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
