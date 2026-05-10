import os
import numpy as np

from video_reader import PyVideoReader

from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.video_processing.input_reader.ReaderInterface import ReaderInterface

class RSVideoReader(ReaderInterface):
    def __init__(self, path_from_project_root : str, config : ReaderConfig):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        self.__width = config.width
        self.__height = config.height
        self.__rotate_param = config.rotate

        filter_vr = f"format=yuv420p,scale=w={self.__width}:h={self.__height}:flags=area"
        # Создается объект cap, проверка на успешное открытие файла
        self.__vr = PyVideoReader(self._path_from_root, filter=filter_vr, oob_mode="skip")

        self.frame_count = int(self.__vr.get_shape()[0])

        self.__gap = int(round(float(self.__vr.get_info()["fps"])) // config.fps)
        if self.__gap < 1:
            self.__gap = 1


    def close(self):
        pass


    def read_all(self) -> np.ndarray:
        frames = self.__vr.decode()
        # frames = frames[..., ::-1].copy()
        return frames

    def read_with_gap(self) -> np.ndarray:
        # frames = self.__vr[::self.__gap]
        frames = self.__vr.get_batch(range(0,self.frame_count,self.__gap))
        # frames = frames[..., ::-1].copy()
        return frames


