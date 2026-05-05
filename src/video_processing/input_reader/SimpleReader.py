import os

import cv2
import numpy as np
from yaml import Loader
from yaml import load

import src.utils.basic_functions.BasicFunctions as bf
from src.video_processing.input_reader.ReaderInterface import ReaderInterface


class SimpleReader(ReaderInterface):
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

        # Создается объект cap, проверка на успешное открытие файла
        self.__cap = cv2.VideoCapture(path_from_project_root)
        if not self.__cap.isOpened():
            raise FileNotFoundError

        self.frame_count = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__curr_cap_frame = 0

    def close(self):
        # Закрывает объект видео
        self.__cap.release()
        cv2.destroyAllWindows()

    def __set_cap_to_first_frame(self):
        """
        Устанавливает позицию текущего кадра на первый кадр видеоряда
        """
        self.__cap.set(1, 0)
        self.__curr_cap_frame = 0

    def __set_cap_to_last_frame(self):
        """
        Устанавливает позицию текущего кадра на последний кадр видеоряда
        """
        self.__cap.set(1, self.frame_count - 1)
        self.__curr_cap_frame = self.frame_count - 1

    def __set_cap_to_n_frame(self, n : int):
        """
        Устанавливает позицию текущего кадра
        :param n: Номер кадра
        """
        if n<0 or n > self.frame_count:
            raise IndexError
        self.__cap.set(1, n)
        self.__curr_cap_frame = n

    def __read_one_frame(self) -> np.ndarray | None:
        """
        Считывает текущий кадр и переходит к следующему, заполняя внутренний список
        :return: Считанный кадр; None при ошибке чтения
        """
        ret, frame = self.__cap.read()
        if ret:
            frame = bf.resize(frame, self.__height, self.__width)
            return frame
        else:
            return None

    def read_all(self) -> list:
        frame_list = list()
        self.__set_cap_to_first_frame()

        frame = self.__read_one_frame()
        while frame is not None:
            frame_list.append(frame)
            self.__curr_cap_frame += 1
            frame = self.__read_one_frame()

        return frame_list

    def read_with_gap(self) -> list:
        frame_list = list()
        self.__set_cap_to_first_frame()

        frame = self.__read_one_frame()
        while frame is not None:
            if self.__curr_cap_frame % self.__gap == 0:
                frame_list.append(frame)
            self.__curr_cap_frame += 1
            frame = self.__read_one_frame()



        return frame_list


