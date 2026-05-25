import os

import cv2
import numpy as np
import src.utils.basic_functions.BasicFunctions as BasicFunctions

from PySide6.QtCore import QObject, Signal
from anyio import sleep
from src.utils.basic_functions.BasicFunctions import rotate
from src.utils.config_readers.BGSubstractorConfig import BGSubstractorConfig
from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.SleepAnalyzerConfig import SleepAnalyzerConfig
from src.utils.config_readers.SleepNetWeightsConfig import SleepNetWeightsConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
from src.utils.file_functions.get_metadata_from_video import get_metadata_from_video
from src.video_processing.input_reader.reader import rsv_read_with_gap
from src.video_processing.vibe_extractor.vibe_extractor import pybind_process_three_channels
from src.video_processing.background_extractor.background_substractor import substract_background
from src.video_processing.motion_intensity_calculator.motion_intensoty_calculator import detect_motion
from src.cnn.SleepNet.classifier import SleepNetClassifier as SleepNetClassifier
from src.sleep_analyser.sleep_analyzer_v1.sleep_analyzer_v1 import SleepAnalyzer_v1

from src.utils.trenslation_manager.translation_manager import _

class VideoProcessor(QObject):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(object)
    error_status = Signal(object)
    cancelled = Signal()

    def __init__(self, video_path, config_path):
        super().__init__()
        self.video_path = video_path
        self.config_path = config_path

        self._stop_flag = False

    def cancel(self):
        self._stop_flag = True

    def run(self):
        try:
            self.status.emit(_("Loading configs"))
            self.progress.emit(0)

            reader_config = ReaderConfig.from_yaml(self.config_path)
            bgs_config = BGSubstractorConfig.from_yaml(self.config_path)
            vibe_config = ViBEConfig.from_yaml(self.config_path)
            analyzer_config = SleepAnalyzerConfig.from_yaml(self.config_path)

            path_to_weights = SleepNetWeightsConfig.from_yaml(self.config_path).path_to_weights

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.status.emit(_("Loading video"))
            self.progress.emit(5)

            frames = rsv_read_with_gap(self.video_path, reader_config)


            if reader_config.rotate:
                frames = np.rot90(frames, k=reader_config.rotate, axes=(1, 2))


            metadata = get_metadata_from_video(self.video_path)

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.status.emit(_("Analyzing presence"))
            self.progress.emit(35)

            masks = substract_background(frames, bgs_config)
            object_presence_list = [(np.sum(masks[i]) / (masks.shape[1] * masks.shape[2])) > 0.05 for i in range(masks.shape[0])]

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.status.emit(_("Analyzing movement intensity"))
            self.progress.emit(45)

            movement_masks = pybind_process_three_channels(frames, vibe_config)

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.progress.emit(60)
            motion_intensity_list = detect_motion(movement_masks, n=5)

            movement_masks = None

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.status.emit(_("Analyzing poses"))
            self.progress.emit(70)

            masks_64 = np.empty(shape=(masks.shape[0], 64, 64), dtype=np.uint8)
            for i in range(masks.shape[0]):
                masks_64[i] = BasicFunctions.get_64pix_mask(masks[i])
            masks = None

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.progress.emit(75)

            classifier = SleepNetClassifier(path_to_weights)
            pose_list = [0 for i in range(frames.shape[0])]
            n_batches = 16
            size_batch = frames.shape[0] // n_batches
            for i in range(n_batches-1):
                pose_list[i*size_batch:(i+1)*size_batch] = classifier.predict_batch(masks_64[i*size_batch:(i+1)*size_batch])

            masks_64 = None

            if self._stop_flag:
                self.cancelled.emit()
                return

            self.status.emit(_("Calculating results"))
            self.progress.emit(85)

            pose_array = np.array(pose_list)
            pose_list = None

            motion_intensity_array = np.array(motion_intensity_list)
            motion_intensity_list = None

            object_presence_array = np.array(object_presence_list)
            object_presence_list = None

            sleep_analyzer = SleepAnalyzer_v1(pose_array=pose_array,
                                              movement_intensity_array=motion_intensity_array,
                                              is_present_array=object_presence_array,
                                              starting_time=metadata['start time'],
                                              framerate=metadata['fps'],
                                              duration = metadata['duration'].in_seconds,
                                              config=analyzer_config
                                              )

            results = sleep_analyzer.get_sleeping_score()

            self.status.emit(_("Done!"))
            self.progress.emit(100)

            self.finished.emit(results)
        except Exception as e:
            self.error_status.emit(e)



