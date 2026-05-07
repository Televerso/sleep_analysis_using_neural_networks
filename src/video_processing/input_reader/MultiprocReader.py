import gc
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import cv2
import src.utils.basic_functions.BasicFunctions as bf
from yaml import load, dump
from yaml import Loader, Dumper

from src.video_processing.input_reader.ReaderInterface import ReaderInterface


# https://medium.com/@haydenfaulkner/extracting-frames-fast-from-a-video-using-opencv-and-python-73b9b7dc9661

class MultiprocReader(ReaderInterface):
    def __init__(self, path_from_project_root : str):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.__num_threads = os.cpu_count()//2

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        # Считываются параметры из конфига
        _config_data = load(open(os.path.join(ROOT_DIR, r"config\reader_config.yml"), 'r'), Loader=Loader)
        self.__width = _config_data['width']
        self.__height = _config_data['height']
        self.__gap = _config_data['gap']
        self.__rotate_param = _config_data['rotate']

        # Создается объект cap, проверка на успешное открытие файла
        cap = cv2.VideoCapture(path_from_project_root)
        if not cap.isOpened():
            raise FileNotFoundError

        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

    def close(self):
        # Закрывает объект видео
        pass


    def _extract_frames(self, start, end, gap, num_worker):
        frame_list = list()
        cap = cv2.VideoCapture(self._path_from_root)  # open the video using OpenCV

        if start < 0:  # if start isn't specified lets assume 0
            start = 0
        if end < 0:  # if end isn't specified assume the end of the video
            end = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cap.set(1, start)  # set the starting frame of the capture
        frame_count = start  # keep track of which frame we are up to, starting from start
        while_safety = 0  # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)

        while frame_count < end:  # lets loop through the frames until the end

            _, frame = cap.read()  # read an image from the capture
            if while_safety > 500:  # break the while if our safety maxs out at 500
                break

            if frame is None:  # if we get a bad return flag or the image we read is None, lets not save
                while_safety += 1  # add 1 to our while safety, since we skip before incrementing our frame variable
                continue  # skip

            if frame_count % gap == 0:  # if this is a frame we want to write out based on the 'every' argument
                frame_list.append(bf.resize(frame, self.__height, self.__width)[:,:,::-1].copy())

            frame_count += 1  # increment our frame count

        cap.release()  # after the while has finished close the capture
        gc.collect()
        return num_worker, frame_list  # and return the count of the images we saved


    def __run_reader(self, gap):
        if self.frame_count < 1:  # if video has no frames, might be and opencv error
            print("Video has no frames. Check your OpenCV + ffmpeg installation")
            return None  # return None

        chunk_size = (self.frame_count // self.__num_threads)
        frame_chunks = [[i, i + chunk_size] for i in
                        range(0, self.frame_count, chunk_size)]  # split the frames into chunk lists
        # make sure last chunk has correct end frame, also handles case chunk_size < total
        frame_chunks[-1][-1] = self.frame_count


        result_list = list()
        # execute across multiple cpu cores to speed up processing, get the count automatically
        with ProcessPoolExecutor(max_workers=self.__num_threads) as executor:
            # submit the processes: extract_frames(...)
            futures = [executor.submit(self._extract_frames, f[0], f[1], gap, i) for i, f in enumerate(frame_chunks)]

            for f in as_completed(futures):  # as each process completes
                i, res = f.result()
                result_list.append([i, np.array(res)])


        result_list.sort(key=lambda x: x[0])

        temp = list()
        for _, res in result_list:
            if res.size != 0:
                temp.append(res)

        result_list = None
        gc.collect()
        result = np.vstack(temp)

        return result


    def read_all(self):
        return self.__run_reader(gap=1)

    def read_with_gap(self):
        return self.__run_reader(gap=self.__gap)
