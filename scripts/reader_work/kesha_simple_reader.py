import os

from src.utils.file_functions.save_frames import save_frames
from src.video_processing.input_reader.DecordReader import DecordReader
from src.video_processing.input_reader.SimpleReader import SimpleReader

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = r"inputs\kesha\video.mp4"
    full_path = os.path.join(ROOT_DIR, video_path)

    save_path = os.path.join(ROOT_DIR, r"outputs\kesha_gap")

    reader1 = SimpleReader(full_path)
    # reader2 = GearReader(full_path)
    reader3 = DecordReader(video_path)

    frames1 = reader1.read_with_gap()
    frames3 = reader3.read_with_gap()

    save_frames(save_path+'1', frames1)
    save_frames(save_path + '3', frames3)

    reader1.close()
    reader3.close()


