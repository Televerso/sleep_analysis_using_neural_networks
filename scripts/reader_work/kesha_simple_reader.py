import os

from src.video_processing.input_reader.DecordReader import DecordReader
from src.video_processing.input_reader.SimpleReader import SimpleReader
from src.video_processing.input_reader.GearReader import GearReader
from src.utils.file_functions.save_frames import save_frames

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = r"inputs\kesha\video.mp4"
    full_path = os.path.join(ROOT_DIR, video_path)

    save_path = os.path.join(ROOT_DIR, r"outputs\kesha")

    # reader = SimpleReader(full_path)
    reader = GearReader(full_path)
    frames = reader.read_all()
    save_frames(save_path, frames)

    reader.close()


