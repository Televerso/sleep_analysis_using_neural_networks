import os
import gc
import src.video_processing.input_reader.Reader as Reader

import time

if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
    video_path = r"inputs\huge_gameplay_video\video_big.mp4"
    full_path = os.path.join(ROOT_DIR, video_path)

    print("Tests for reading all frames: ")

    start = time.time()
    Reader.decord_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with decord: {end - start}")

    start = time.time()
    Reader.gear_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with camgear: {end - start}")

    start = time.time()
    Reader.rsv_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with video-reader-rs: {end - start}")

    start = time.time()
    Reader.cv2_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with native open-cv: {end - start}")

    start = time.time()
    Reader.mp_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with python multiprocessing: {end - start}")

    start = time.time()
    Reader.mpsm_read_all(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading all frames with python multiprocessing with shared memory: {end - start}")

    print('\n', "Tests for reading frames with gaps: ")

    start = time.time()
    Reader.decord_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with decord: {end - start}")

    start = time.time()
    Reader.gear_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with camgear: {end - start}")

    start = time.time()
    Reader.rsv_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with video-reader-rs: {end - start}")

    start = time.time()
    Reader.cv2_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with native open-cv: {end - start}")

    start = time.time()
    Reader.mp_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with python multiprocessing: {end - start}")

    start = time.time()
    Reader.mpsm_read_with_gap(full_path)
    end = time.time()
    gc.collect()
    print(f"Time for reading frames with gaps with python multiprocessing with shared memory: {end - start}")








