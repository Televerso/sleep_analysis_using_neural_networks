import os
import numpy as np

import src.utils.basic_functions.BasicFunctions as bf
from video_reader import PyVideoReader
from yaml import load, dump
from yaml import Loader, Dumper

from src.video_processing.input_reader.ReaderInterface import ReaderInterface

class RSVideoReader(ReaderInterface):
    def __init__(self, path_from_project_root : str):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        # Считываются параметры из конфига
        _config_data = load(open(os.path.join(ROOT_DIR, r"config\reader_config.yml"), 'r'), Loader=Loader)
        self.__width = _config_data['width']
        self.__height = _config_data['height']
        self.__gap = _config_data['gap']
        self.__rotate_param = _config_data['rotate']

        filter_vr = f"format=yuv420p,scale=w={self.__width}:h={self.__height}:flags=area"
        # Создается объект cap, проверка на успешное открытие файла
        self.__vr = PyVideoReader(self._path_from_root, filter=filter_vr, oob_mode="skip")

        self.frame_count = int(self.__vr.get_shape()[0])


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


