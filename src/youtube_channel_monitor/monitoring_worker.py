import asyncio
import logging

from youtube_channel_monitor import monitoring_service

from .repositories import database
from .repositories.channel_repository import ChannelRepository

logger = logging.getLogger(__name__)


def run_monitor(stop_event, interval_seconds):
    while not stop_event.is_set():
        try:
            with database.transaction() as connection:
                channels = ChannelRepository(connection).get_channels()

            monitoring_service.check_for_new_videos(channels)
        except Exception:
            logger.exception("New videos check failed")

        stop_event.wait(interval_seconds)


async def watch_monitor_status(monitor_thread, stop_event, server):
    while not stop_event.is_set():
        if monitor_thread.is_alive():
            await asyncio.sleep(10)
        else:
            server.should_exit = True
            logger.critical("Monitor thread has failed. Starting server shutdown...")
            break
