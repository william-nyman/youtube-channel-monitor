import pathlib

from storage import (
    create_channels_table,
    create_videos_table,
    return_list_of_channels_in_db,
)
from youtube import check_for_new_video, get_youtube_channel

pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

def main():
    create_videos_table()
    create_channels_table()

    get_youtube_channel()
    check_for_new_video(return_list_of_channels_in_db())




if __name__ == "__main__":
    main()
