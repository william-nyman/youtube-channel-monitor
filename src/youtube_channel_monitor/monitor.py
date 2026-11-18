import logging
import threading

import uvicorn

from . import config, storage, youtube

logger = logging.getLogger(__name__)


def run_monitor(stop_event, interval_seconds):
    while not stop_event.is_set():
        try:
            youtube.check_for_new_video(storage.get_channels())
        except Exception:
            logger.exception("New videos check failed")

        stop_event.wait(interval_seconds)


def main():
    stop_event = threading.Event()

    monitor_thread = threading.Thread(
        target=run_monitor, args=(stop_event, config.interval_minutes())
    )

    monitor_thread.start()

    try:
        uvicorn.run(
            "youtube_channel_monitor.api:app",
            host="0.0.0.0",
            port=8000,
            workers=1,
        )
    finally:
        stop_event.set()
        monitor_thread.join()
