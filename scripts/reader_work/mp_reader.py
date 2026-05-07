import os

from src.video_processing.input_reader.MultiprocReader import MultiprocReader
from src.utils.file_functions.save_frames import save_frames

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    # video_path = r"inputs\huge_gameplay_video\video.mp4"
    video_path = r"inputs\kesha\video.mp4"
    full_path = os.path.join(ROOT_DIR, video_path)

    save_path = os.path.join(ROOT_DIR, r"outputs\kesha_gap")

    reader = MultiprocReader(full_path)

    frames = reader.read_with_gap()

    save_frames(save_path + 'mp', frames)


