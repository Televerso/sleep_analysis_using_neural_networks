import os

from decord import VideoReader
from yaml import Loader
from yaml import load

from src.video_processing.input_reader.ReaderInterface import ReaderInterface


class DecordReader(ReaderInterface):
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
        self.__vr = VideoReader(self._path_from_root, width=self.__width, height=self.__height)

        self.frame_count = int(len(self.__vr))


    def close(self):
        self.__vr = None


    def read_all(self) -> list:
        frames = self.__vr.get_batch(list(range(0, self.frame_count))).asnumpy()
        frame_list = [i[:,:,::-1] for i in frames]
        return frame_list

    def read_with_gap(self) -> list:
        frames = self.__vr.get_batch(list(range(0, self.frame_count, self.__gap))).asnumpy()
        frame_list = [i[:,:,::-1] for i in frames]
        return frame_list


