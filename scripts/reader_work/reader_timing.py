import os
import gc
import src.video_processing.input_reader.Reader as Reader

import time

from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig


def time_all(full_path, config):
    print("Tests for reading all frames: ")

    start = time.time()
    Reader.decord_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with decord: {end - start}")

    start = time.time()
    Reader.gear_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with camgear: {end - start}")

    start = time.time()
    Reader.rsv_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with video-reader-rs: {end - start}")

    start = time.time()
    Reader.pyav_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with PyAV: {end - start}")

    start = time.time()
    Reader.cv2_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with native open-cv: {end - start}")

    start = time.time()
    Reader.mp_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with python multiprocessing: {end - start}")

    start = time.time()
    Reader.mpsm_read_all(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with python multiprocessing with shared memory: {end - start}")


def time_with_gap(full_path, config):
    print('\n', "Tests for reading frames with gaps: ")

    start = time.time()
    Reader.decord_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with decord: {end - start}")

    start = time.time()
    Reader.gear_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with camgear: {end - start}")

    start = time.time()
    Reader.rsv_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with video-reader-rs: {end - start}")

    start = time.time()
    Reader.pyav_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with PyAV: {end - start}")

    start = time.time()
    Reader.cv2_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with native open-cv: {end - start}")

    start = time.time()
    Reader.mp_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with python multiprocessing: {end - start}")

    start = time.time()
    Reader.mpsm_read_with_gap(full_path, config)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with python multiprocessing with shared memory: {end - start}")

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    # video_path = r"inputs\test_sleeping_video\video.mp4"
    # video_path = r"inputs\huge_gameplay_video\video.mp4"
    video_path = r"inputs\12h_test_video\video.mp4"
    # video_path = r"inputs\kesha\video.mp4"
    config_path = r"config\config.yml"
    full_path = os.path.join(ROOT_DIR, video_path)
    config = ReaderConfig.from_yaml(os.path.join(ROOT_DIR, config_path))

    # time_all(full_path, config)

    time_with_gap(full_path, config)












