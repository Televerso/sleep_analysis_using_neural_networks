import os
import numpy as np

from src.utils.config_readers.ReaderConfig import ReaderConfig
from decord import VideoReader

from src.video_processing.input_reader.ReaderInterface import ReaderInterface

class DecordReader(ReaderInterface):
    def __init__(self, path_from_project_root : str, config : ReaderConfig):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        self.__width = config.width
        self.__height = config.height
        self.__rotate_param = config.rotate

        # Создается объект cap, проверка на успешное открытие файла
        self.__vr = VideoReader(self._path_from_root, width=self.__width, height=self.__height)

        self.__gap = int(round(self.__vr.get_avg_fps()) // config.fps)
        if self.__gap < 1:
            self.__gap = 1

        self.frame_count = int(len(self.__vr))


    def close(self):
        pass


    def read_all(self) -> np.ndarray:
        frames = self.__vr.get_batch(list(range(0, self.frame_count))).asnumpy()
        return frames

    def read_with_gap(self) -> np.ndarray:
        frames = self.__vr.get_batch(list(range(0, self.frame_count, self.__gap))).asnumpy()
        return frames


