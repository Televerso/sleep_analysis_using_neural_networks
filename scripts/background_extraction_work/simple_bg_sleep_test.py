import os

import src.video_processing.background_extractor.simple_background_extractor as sb
from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.file_functions.save_frames import save_frames
from src.video_processing.input_reader.reader import rsv_read_all, rsv_read_with_gap

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = os.path.join(ROOT_DIR, r'inputs\test_sleeping_video\video.mp4')
    config = ReaderConfig().from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))
    config.fps = 1
    frames = rsv_read_with_gap(video_path, config)

    sb_ext = sb.SimpleBackgroundExtractor(frames[-1], 60)

    masks = list()
    for frame in frames:
        masks.append(sb_ext.detect(frame))

    save_frames(os.path.join(ROOT_DIR, r'outputs\background_sleep'), masks)