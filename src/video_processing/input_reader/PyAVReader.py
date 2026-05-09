import av

import os

import numpy as np
import src.utils.basic_functions.BasicFunctions as bf
from yaml import load, dump
from yaml import Loader, Dumper

from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig
from src.video_processing.input_reader.ReaderInterface import ReaderInterface

class PyAVReader(ReaderInterface):
    def __init__(self, path_from_project_root : str, config : ReaderConfig):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        self.__width = config.width
        self.__height = config.height
        self.__rotate_param = config.rotate

        # Создается объект cap, проверка на успешное открытие файла
        self.__container = av.open(path_from_project_root)
        self.__stream = self.__container.streams.video[0]
        self.__stream.thread_type = "AUTO"

        self.frame_count = self.__stream.frames
        self.__gap = int(round(self.__stream.average_rate) // config.fps)
        if self.__gap < 1:
            self.__gap = 1

        self.__curr_frame = 0

    def close(self):
        # Закрывает объект видео
        self.__container.close()


    def read_all(self) -> np.ndarray:
        frame_list = list()

        self.__container.seek(0)

        for frame in self.__container.decode(self.__stream):
            frame_list.append(bf.resize(frame.to_ndarray(format="rgb24"), self.__height, self.__width))

        return np.array(frame_list)

    def read_with_gap(self) -> np.ndarray:
        frame_list = list()

        self.__container.seek(0)

        for i, frame in enumerate(self.__container.decode(self.__stream)):
            if i % self.__gap == 0:
                frame_list.append(bf.resize(frame.to_ndarray(format="rgb24"), self.__height, self.__width))

        return np.array(frame_list)


