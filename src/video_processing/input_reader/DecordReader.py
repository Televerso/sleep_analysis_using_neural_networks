import os
import numpy as np

import src.utils.basic_functions.BasicFunctions as bf
from decord import VideoReader
from yaml import load, dump
from yaml import Loader, Dumper

from src.video_processing.input_reader.ReaderInterface import ReaderInterface

class DecordReader(ReaderInterface):
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
        self.vr = VideoReader(self.path_from_root, width=self.__width, height=self.__height)

        self.frame_count = int(len(self.vr))
        self.curr_vr_frame = 0

    def close(self):
        self.vr = None

    def __set_it_to_first_frame(self):
        """
        Устанавливает позицию текущего кадра на первый кадр видеоряда
        """
        self.curr_frame = 0

    def __set_it_to_last_frame(self):
        """
        Устанавливает позицию текущего кадра на последний кадр видеоряда
        """
        self.curr_frame = self.frame_count - 1

    def __set_it_to_n_frame(self, n : int):
        """
        Устанавливает позицию текущего кадра
        :param n: Номер кадра
        """
        if n<0 or n > self.frame_count:
            raise IndexError
        self.curr_frame = n

    def __read_one_frame(self) -> np.ndarray | None:
        """
        Считывает текущий кадр и переходит к следующему, заполняя внутренний список
        :return: Считанный кадр; None при ошибке чтения
        """
        frame = self.vr[self.curr_vr_frame].asnumpy()
        if self.curr_vr_frame+1 >= self.frame_count:
            self.curr_frame += 1
            return frame
        else:
            return None

    def read_all(self) -> list:
        frames = self.vr.get_batch(list(range(0, self.frame_count))).asnumpy()
        frame_list = [i[:,:,::-1] for i in frames]
        self.__set_it_to_last_frame()
        return frame_list

    def read_with_gap(self) -> list:
        frames = self.vr.get_batch(list(range(0,self.frame_count,self.__gap))).asnumpy()
        frame_list = [i[:,:,::-1] for i in frames]
        self.__set_it_to_last_frame()
        return frame_list


