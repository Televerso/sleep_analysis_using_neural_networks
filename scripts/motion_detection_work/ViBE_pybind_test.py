import VibeExtractor as ve
import os

from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig
from src.utils.file_functions.config_readers.ViBEConfig import ViBEConfig
from src.utils.file_functions.save_frames import save_frames
from src.video_processing.input_reader.Reader import rsv_read_all
import src.video_processing.ViBE_extractor_pybind.ViBEWrapperPybind as ViBEWrapper


if __name__ == '__main__':
    N = 20
    R = 40
    _min = 2
    phi = 16

    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = os.path.join(ROOT_DIR, r'inputs\kesha\video.mp4')
    output_path = os.path.join(ROOT_DIR, r'outputs\kesha_mas')

    config = ReaderConfig.from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))

    frames = rsv_read_all(video_path, config)

    config = ViBEConfig.from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))

    out_frames = ViBEWrapper.process_frames_three_channels(frames, config)

    save_frames(output_path, out_frames)

