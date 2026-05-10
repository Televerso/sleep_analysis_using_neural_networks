import VibeExtractor as ve
import os

from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig
from src.utils.file_functions.save_frames import save_frames
from src.video_processing.input_reader.Reader import rsv_read_all


if __name__ == '__main__':
    N = 20
    R = 40
    _min = 2
    phi = 16

    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = os.path.join(ROOT_DIR, r'inputs\kesha\video.mp4')
    save_path = os.path.join(ROOT_DIR, r"outputs\kesha_reg")
    output_path = os.path.join(ROOT_DIR, r'outputs\kesha_mas')

    config = ReaderConfig().from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))

    frames = rsv_read_all(video_path, config)
    save_frames(save_path, frames)

    ViBE = ve.VibeAlgorithm(frames[-1,:,:,0],N,R,_min,phi)
    out_frames = list()
    for frame in frames:
        out_frames.append(ViBE.vibe_detection(frame[:,:,0].copy()))

    save_frames(output_path, out_frames)

