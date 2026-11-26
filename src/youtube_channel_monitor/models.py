from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Video:
    yt_videoid: str
    title: str
    link: str
    name: str
    published: str
    thumbnail: str
    channel_id: str


@dataclass
class Channel:
    channel_id: str
    name: str
    monitor_shorts: bool = False
    added_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
