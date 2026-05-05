import os
from threading import Lock

import cv2
from vidgear.gears import CamGear
from yaml import Loader
from yaml import load

import src.utils.basic_functions.BasicFunctions as bf
from src.video_processing.input_reader.ReaderInterface import ReaderInterface


class GearReader(ReaderInterface):
    def __init__(self, path_from_project_root: str):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        # Считываются параметры из конфига
        _config_data = load(open(os.path.join(ROOT_DIR, r"config\reader_config.yml"), 'r'), Loader=Loader)
        self.__width = _config_data['width']
        self.__height = _config_data['height']
        self.__gap = _config_data['gap']
        self.__rotate_param = _config_data['rotate']

        # Создается объект stream
        __options = {
            "CAP_PROP_FRAME_WIDTH": self.__width,
            "CAP_PROP_FRAME_HEIGHT": self.__height,
        }
        self.__stream = CamGear(self._path_from_root, **__options).start()

        self.frame_count = int(self.__stream.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__lock = Lock()
        self.__curr_cap_frame = 0

    def close(self):
        # Закрывает объект видео
        self.__stream.stop()


    def read_all(self) -> list:
        frame_list = list()

        frame = self.__stream.read()
        while frame is not None:
            frame_list.append(frame)
            frame = self.__stream.read()

        with self.__lock:
            for i in range(len(frame_list)):
                frame_list[i] = bf.resize(frame_list[i], self.__height, self.__width)

        return frame_list


    def read_with_gap(self) -> list:
        frame_list = list()

        frame = self.__stream.read()

        while frame is not None:
            with self.__lock:
                curr_frame = self.__curr_cap_frame
                self.__curr_cap_frame += 1

            if curr_frame % self.__gap == 0:
                frame_list.append(frame)
            frame = self.__stream.read()

        with self.__lock:
            for i in range(len(frame_list)):
                frame_list[i] = bf.resize(frame_list[i], self.__height, self.__width)

        return frame_list
