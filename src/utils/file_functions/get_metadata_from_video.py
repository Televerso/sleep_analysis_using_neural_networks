import os
from datetime import datetime

import cv2

from src.utils.data_structures.SleepTime import SleepTime


def get_metadata_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()

    if fps <= 0 or total_frames <= 0:
        raise ValueError("Could not retrieve valid FPS or frame count.")

    duration_seconds = total_frames // fps
    duration_time = SleepTime(hour=(duration_seconds // 3600) % 24,
                              minute=(duration_seconds // 60) % 60,
                              second=(duration_seconds % 3600) % 60)

    creation_datetime = datetime.fromtimestamp(os.path.getctime(video_path))
    creation_time = SleepTime(creation_datetime.hour, creation_datetime.minute, creation_datetime.second)


    info_dict = {"fps": fps, "duration": duration_time, "start time": creation_time - duration_time,
                 "end time": creation_time}

    return info_dict