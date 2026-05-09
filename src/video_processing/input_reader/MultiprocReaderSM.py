import gc
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import shared_memory, Lock, Pool

import numpy as np
import cv2
import src.utils.basic_functions.BasicFunctions as bf
from yaml import load, dump
from yaml import Loader, Dumper

from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig
from src.video_processing.input_reader.ReaderInterface import ReaderInterface

_worker_lock = None


def _worker_initializer(lock):
    global _worker_lock
    _worker_lock = lock

class SharedOutputBuffer:
    def __init__(self, max_frames, height, width, channels=3):
        # Allocate for worst case
        self.__max_frames = max_frames
        self.__frame_size = height * width * channels

        # Shared memory for: [counter, padding..., frames...]
        # First 8 bytes: atomic counter of frames written
        self.__total_size = 8 + (max_frames * self.__frame_size)

        self._shm = shared_memory.SharedMemory(create=True, size=self.__total_size)
        self._counter = np.ndarray(1, dtype=np.int64, buffer=self._shm.buf[:8])
        self._counter[0] = 0

        # The frame buffer starts after the counter
        self._frames = np.ndarray(
            (max_frames, height, width, channels),
            dtype=np.uint8,
            buffer=self._shm.buf[8:]
        )


    def get_results(self):
        """Parent calls this to get all collected frames"""
        count = self._counter[0]
        return self._frames[:count].copy()

    def cleanup(self):
        self._shm.close()
        self._shm.unlink()


class MultiprocReaderSM(ReaderInterface):
    def __init__(self, path_from_project_root : str, config : ReaderConfig):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.__num_threads = os.cpu_count()//2

        # Путь к видео из корневой директории
        self._path_from_root = os.path.join(ROOT_DIR, path_from_project_root)

        self.__width = config.width
        self.__height = config.height
        self.__rotate_param = config.rotate

        # Создается объект cap, проверка на успешное открытие файла
        cap = cv2.VideoCapture(path_from_project_root)
        if not cap.isOpened():
            raise FileNotFoundError
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.__gap = int(round(cap.get(cv2.CAP_PROP_FPS)) // config.fps)
        if self.__gap < 1:
            self.__gap = 1

        cap.release()

        self.__max_frames = None


    def close(self):
        # Закрывает объект видео
        pass


    def _extract_frames(self, start, end, gap, num_worker, shm_name):
        global _worker_lock

        # Reconnect to shared memory
        shm = shared_memory.SharedMemory(name=shm_name)
        counter = np.ndarray((1,), dtype=np.int64, buffer=shm.buf[:8])
        frames = np.ndarray(
            (self.__max_frames, self.__height, self.__width, 3),
            dtype=np.uint8,
            buffer=shm.buf[8:]
        )
        cap = cv2.VideoCapture(self._path_from_root)
        if start < 0:  # if start isn't specified lets assume 0
            start = 0
        if end < 0:  # if end isn't specified assume the end of the video
            end = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cap.set(1, start)
        additions_counter = 0
        frame_counter = start
        while frame_counter < end:
            _, frame = cap.read()
            if frame_counter % gap == 0:
                frame = bf.resize(frame, self.__height, self.__width)[:, :, ::-1]
                with _worker_lock:
                    current = counter[0]
                    frames[frame_counter // gap] = frame
                    counter[0] = current + 1
                additions_counter += 1
            frame_counter += 1
        cap.release()
        shm.close()
        return num_worker


    def __run_reader(self, gap):
        buffer = SharedOutputBuffer(self.__max_frames, self.__height, self.__width, 3)

        chunk_size = (self.frame_count // self.__num_threads)
        frame_chunks = [[i, i + chunk_size] for i in
                        range(0, self.frame_count, chunk_size)]  # split the frames into chunk lists

        # make sure last chunk has correct end frame, also handles case chunk_size < total
        frame_chunks[-1][-1] = self.frame_count

        lock = Lock()

        with Pool(processes=self.__num_threads,
                  initializer=_worker_initializer,
                  initargs=(lock,)) as pool:
            results = pool.starmap(
                self._extract_frames,
                [
                    (
                        frame_chunks[i][0],
                        frame_chunks[i][1],
                        gap,
                        i,
                        buffer._shm.name,
                    )
                 for i in range(len(frame_chunks))
                ]
            )

        result = buffer.get_results()
        buffer.cleanup()
        return result

    def read_all(self):
        self.__max_frames = self.frame_count
        return self.__run_reader(gap=1)

    def read_with_gap(self):
        self.__max_frames = 1 + self.frame_count // self.__gap
        return self.__run_reader(gap=self.__gap)
