from storage import return_list_of_channels_in_db
from youtube import check_for_new_video, get_youtube_channel


def main():

    get_youtube_channel()
    check_for_new_video(return_list_of_channels_in_db())



if __name__ == "__main__":
    main()
