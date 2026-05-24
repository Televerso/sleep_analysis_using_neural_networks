import cv2
from PySide6.QtCore import QObject
from PySide6.QtGui import QImage
from src.utils.file_functions.get_metadata_from_video import get_metadata_from_video
import yaml


class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.config_path = None
        self.results = None


    def generate_preview(self, file_path):
        cap = cv2.VideoCapture(file_path)
        ret, image = cap.read()
        if not ret:
            cap.release()
            raise FileNotFoundError
        image = cv2.resize(image, (160, 120))
        cap.release()

        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()

        info_dict = {key : str(val) for key,val in get_metadata_from_video(file_path).items()}

        return qt_image, info_dict

    def read_config(self):
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f)
        return data

    def save_config(self, config):
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False, default_flow_style=False)


