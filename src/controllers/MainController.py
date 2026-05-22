import os

import cv2
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QImage, QPixmap

from src.models import video_processor
from src.views.ErrorWindow import ErrorWindow


class MainController(QObject):
    error_msg = Signal(str)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.error_view = None
        self.model = model

        self._worker = None
        self._thread = None

        self.view.file_selected.connect(self.on_file_selected)
        self.view.start_processing.connect(self.on_start_pressed)


    def process_exeption(self, exception):
        self.error_view = ErrorWindow()
        self.error_view.set_error_msg(str(exception))
        self.error_view.show()

    def on_file_selected(self, file_path):
        try:
            qt_image, info_dict = self.model.generate_preview(file_path)
            self.view.update_preview(qt_image, info_dict)
            self.model.video_path = file_path
        except Exception as e:
            self.process_exeption(e)


    def on_start_pressed(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        try:
            video_path = self.model.video_path
            config_path = os.path.join(ROOT_DIR, 'config', 'config.yml')
            if not video_path:
                raise FileNotFoundError("No file selected")

            self._thread = QThread()
            self._worker = video_processor.VideoProcessor(video_path, config_path)
            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._worker.progress.connect(self.view.update_progress)
            self._worker.status.connect(self.view.update_status)
            self._worker.finished.connect(self._on_processing_finished)
            self._worker.error_status.connect(self._on_processing_error)

            self._worker.finished.connect(self._thread.quit)
            self._worker.finished.connect(self._worker.deleteLater)
            self._thread.finished.connect(self._thread.deleteLater)

            # Start!
            self._thread.start()

        except Exception as e:
            self.view.start_button.setEnabled(True)
            self.process_exeption(e)

    def _on_processing_finished(self, results):
        self.model.results = results
        self.view.display_results(results)

    def _on_processing_error(self, error):
        self.view.start_button.setEnabled(True)
        self.process_exeption(error)