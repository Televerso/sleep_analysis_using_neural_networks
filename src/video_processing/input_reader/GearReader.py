import os
import numpy as np

import src.utils.basic_functions.BasicFunctions as bf
from vidgear.gears import CamGear
import cv2
from yaml import load, dump
from yaml import Loader, Dumper

from src.video_processing.input_reader.Reader import Reader

class GearReader(Reader):
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
        print("Video file opened successfully!")

        self.frame_count = int(self.stream.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.curr_cap_frame = 0

    def close(self):
        # Закрывает объект видео
        cv2.destroyAllWindows()
        self.stream.stop()


    def __set_cap_to_first_frame(self):
        """
        Устанавливает позицию текущего кадра на первый кадр видеоряда
        """
        self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.curr_cap_frame = 0

    def __set_cap_to_last_frame(self):
        """
        Устанавливает позицию текущего кадра на последний кадр видеоряда
        """
        self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, self.frame_count-1)
        self.curr_cap_frame = self.frame_count - 1

    def __set_cap_to_n_frame(self, n: int):
        """
        Устанавливает позицию текущего кадра
        :param n: Номер кадра
        """
        if n < 0 or n > self.frame_count:
            raise IndexError
        self.stream.stream.set(cv2.CAP_PROP_POS_FRAMES, n)
        self.curr_cap_frame = n

    def __read_one_frame(self) -> np.ndarray | None:
        """
        Считывает текущий кадр и переходит к следующему, заполняя внутренний список
        :return: Считанный кадр; None при ошибке чтения
        """
        frame = self.stream.read()
        self.curr_cap_frame += 1
        return frame

    def read_all(self) -> list:
        frame_list = list()

        frame = self.stream.read()
        while frame is not None:
            frame_list.append(frame)
            self.curr_cap_frame += 1
            frame = self.stream.read()

        self.curr_cap_frame = self.frame_count - 1
        return frame_list

    def read_with_gap(self) -> list:
        frame_list = list()

        frame = self.stream.read()
        while frame is not None:
            if self.curr_cap_frame % self.__gap == 0:
                frame_list.append(frame)
            self.curr_cap_frame += 1
            frame = self.stream.read()

        self.curr_cap_frame = self.frame_count - 1
        return frame_list
