import os
import sys

import numpy as np
import cv2
import src.utils.basic_functions.BasicFunctions as bf
from yaml import load, dump
from yaml import Loader, Dumper

class SimpleReader:
    def __init__(self, path_from_project_root : str):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        # Путь к видео из корневой директории
        self.path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        # Считываются параметры из конфига
        config_data = load(open(os.path.join(ROOT_DIR, r"config\reader_config.yml"), 'r'), Loader=Loader)
        self.__width = config_data['width']
        self.__height = config_data['height']
        self.__gap = config_data['gap']
        self.__rotate_param = config_data['rotate']

        # Создается объект cap, проверка на успешное открытие файла
        self.cap = cv2.VideoCapture(path_from_project_root)
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            raise FileNotFoundError
        else:
            print("Video file opened successfully!")

        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.curr_cap_frame = 0

    def __del__(self):
        # Закрывает объект видео
        # self.cap.release()
        cv2.destroyAllWindows()

    def __set_cap_to_first_frame(self):
        """
        Устанавливает позицию текущего кадра на первый кадр видеоряда
        """
        self.cap.set(1, 0)
        self.curr_cap_frame = 0

    def __set_cap_to_last_frame(self):
        """
        Устанавливает позицию текущего кадра на последний кадр видеоряда
        """
        self.cap.set(1, self.frame_count - 1)
        self.curr_cap_frame = self.frame_count - 1

    def __set_cap_to_n_frame(self, n : int):
        """
        Устанавливает позицию текущего кадра
        :param n: Номер кадра
        """
        self.cap.set(1, n)
        self.curr_cap_frame = n

    def __read_one_frame(self) -> np.ndarray | None:
        """
        Считывает текущий кадр и переходит к следующему, заполняя внутренний список
        :return: Считанный кадр; None при ошибке чтения
        """
        ret, frame = self.cap.read()
        if ret:
            frame = bf.resize(frame, self.__height, self.__width)
            self.curr_cap_frame += 1
            return frame
        else:
            return None

    def read_all(self) -> list:
        frame_list = list()
        self.__set_cap_to_first_frame()

        frame = self.__read_one_frame()
        while frame is not None:
            frame_list.append(frame)
            frame = self.__read_one_frame()

        return frame_list

    def read_with_gap(self) -> list:
        frame_list = list()
        self.__set_cap_to_first_frame()

        frame = self.__read_one_frame()
        while frame is not None:
            if self.curr_cap_frame % self.__gap == 0:
                frame_list.append(frame)
            frame = self.__read_one_frame()

        return frame_list


