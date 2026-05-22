import os
import numpy as np
import src.utils.basic_functions.BasicFunctions as BasicFunctions

from PySide6.QtCore import QObject, Signal
from anyio import sleep
from src.utils.config_readers.BGSubstractorConfig import BGSubstractorConfig
from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
from src.video_processing.input_reader.reader import rsv_read_with_gap
from src.video_processing.vibe_extractor.vibe_extractor import pybind_process_three_channels
from src.video_processing.background_extractor.background_substractor import substract_background
from src.cnn.SleepNet.classifier import SleepNetClassifier as SleepNetClassifier

class VideoProcessor(QObject):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(object)
    error_status = Signal(object)

    def __init__(self, video_path, config_path):
        super().__init__()
        self.video_path = video_path
        self.config_path = config_path

    def run(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        path_to_weights = os.path.join(ROOT_DIR, "data", "models", "SleepNet", "SleepNet_v6.pth")

        try:
            self.status.emit("Loading configs")
            self.progress.emit(0)

            reader_config = ReaderConfig.from_yaml(self.config_path)
            bgs_config = BGSubstractorConfig.from_yaml(self.config_path)
            vibe_config = ViBEConfig.from_yaml(self.config_path)

            self.status.emit("Loading video")
            self.progress.emit(5)

            frames = rsv_read_with_gap(self.video_path, reader_config)

            self.status.emit("Analyzing presence")
            self.progress.emit(35)

            masks = substract_background(frames, bgs_config)

            self.status.emit("Analyzing movement intensity")
            self.progress.emit(45)

            movement_masks = pybind_process_three_channels(frames, vibe_config)

            self.status.emit("Analyzing poses")
            self.progress.emit(70)

            masks_64 = np.empty(shape=(masks.shape[0], 64, 64), dtype=np.uint8)

            for i in range(frames.shape[0]):
                masks_64[i] = BasicFunctions.get_64pix_mask(masks[i])

            classifier = SleepNetClassifier(path_to_weights)
            pose_list = [0 for i in range(frames.shape[0])]
            n_batches = 16
            size_batch = frames.shape[0] // n_batches
            for i in range(n_batches-1):
                pose_list[i*size_batch:(i+1)*size_batch] = classifier.predict_batch(masks_64[i*size_batch:(i+1)*size_batch])

            self.status.emit("Compiling results")
            self.progress.emit(85)

            sleep(5)

            self.status.emit("Done!")
            self.progress.emit(100)
            self.finished.emit(None)
        except Exception as e:
            self.error_status.emit(e)


