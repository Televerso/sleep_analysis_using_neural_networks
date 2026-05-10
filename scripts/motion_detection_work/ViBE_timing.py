import os
import time

from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
from src.video_processing.ViBE_extractor_pybind import ViBEWrapperPybind
from src.video_processing.input_reader.Reader import rsv_read_all
import src.video_processing.ViBE_extractor_native_py.ViBEWrapperNative as ViBEWrapperNative


def time_three_channels(frames, config):
    start = time.time()
    ViBEWrapperNative.process_frames_three_channels(frames, config)
    end = time.time()
    time_native = end - start
    print("Time for native python for three channels: ", time_native)

    start = time.time()
    ViBEWrapperPybind.process_frames_three_channels(frames, config)
    end = time.time()
    time_pybind = end - start
    print("Time for pybind for three channels: ", time_pybind)

    print("General speedup = ", time_native / time_pybind)


def time_single_channel(frames, config):
    start = time.time()
    ViBEWrapperNative.process_frames_single_channel(frames, config)
    end = time.time()
    time_native = end - start
    print("Time for native python for single channel: ", time_native)

    start = time.time()
    ViBEWrapperPybind.process_frames_single_channel(frames, config)
    end = time.time()
    time_pybind = end - start
    print("Time for pybind for single channel: ", time_pybind)

    print("General speedup = ", time_native / time_pybind)


if __name__ == '__main__':
    ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

    video_path = os.path.join(ROOT_DIR, r'inputs\kesha\video.mp4')

    config = ReaderConfig().from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))
    frames = rsv_read_all(video_path, config)

    config = ViBEConfig.from_yaml(os.path.join(ROOT_DIR, r'config\config.yml'))

    print("Measuring time for a single color channel: ")
    time_single_channel(frames[:,:,:,2], config)

    print("Measuring time for three color channels: ")
    time_three_channels(frames, config)










