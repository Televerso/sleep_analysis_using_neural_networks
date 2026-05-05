import os
import numpy as np

from vidgear.gears import CamGear
import cv2
from threading import Lock
from yaml import load, dump
from yaml import Loader, Dumper

from src.video_processing.input_reader.ReaderInterface import ReaderInterface

import src.utils.basic_functions.BasicFunctions as bf

class GearReader(ReaderInterface):
    def __init__(self, path_from_project_root: str):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self.path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        # Считываются параметры из конфига
        config_data = load(open(os.path.join(ROOT_DIR, r"config\reader_config.yml"), 'r'), Loader=Loader)
        self.__width = config_data['width']
        self.__height = config_data['height']
        self.__gap = config_data['gap']
        self.__rotate_param = config_data['rotate']

        # Создается объект stream
        options = {
            "CAP_PROP_FRAME_WIDTH": self.__width,
            "CAP_PROP_FRAME_HEIGHT": self.__height,
        }
        self.stream = CamGear(self.path_from_root, **options).start()

        self.frame_count = int(self.stream.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__lock = Lock()
        self.curr_cap_frame = 0

    def close(self):
        # Закрывает объект видео
        self.stream.stop()


    def __set_cap_to_first_frame(self):
        """
        Устанавливает позицию текущего кадра на первый кадр видеоряда
        """
        with self.__lock:
            self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.curr_cap_frame = 0

    def __set_cap_to_last_frame(self):
        """
        Устанавливает позицию текущего кадра на последний кадр видеоряда
        """
        with self.__lock:
            self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, self.frame_count-1)
            self.curr_cap_frame = self.frame_count - 1

    def __set_cap_to_n_frame(self, n: int):
        """
        Устанавливает позицию текущего кадра
        :param n: Номер кадра
        """
        if n < 0 or n > self.frame_count:
            raise IndexError
        with self.__lock:
            self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, n)
            self.curr_cap_frame = n

    def __read_one_frame(self) -> np.ndarray | None:
        """
        Считывает текущий кадр и переходит к следующему, заполняя внутренний список
        :return: Считанный кадр; None при ошибке чтения
        """
        frame = self.stream.read()
        with self.__lock:
            self.curr_cap_frame += 1
        return frame

    def read_all(self) -> list:
        frame_list = list()

        frame = self.__read_one_frame()
        while frame is not None:
            frame_list.append(frame)
            frame = self.__read_one_frame()

        self.__set_cap_to_last_frame()

        with self.__lock:
            for i in range(len(frame_list)):
                frame_list[i] = bf.resize(frame_list[i], self.__height, self.__width)
        return frame_list

    def read_with_gap(self) -> list:
        frame_list = list()

        frame = self.__read_one_frame()
        with self.__lock:
            self.curr_cap_frame = 0

        while frame is not None:
            with self.__lock:
                curr_frame = self.curr_cap_frame
                self.curr_cap_frame += 1

            if curr_frame % self.__gap == 0:
                frame_list.append(frame)
            frame = self.stream.read()

        self.__set_cap_to_last_frame()

        with self.__lock:
            for i in range(len(frame_list)):
                frame_list[i] = bf.resize(frame_list[i], self.__height, self.__width)

        return frame_list
