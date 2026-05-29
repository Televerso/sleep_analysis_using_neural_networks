import os

import cv2
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication

from src.models import video_processor
from src.utils.file_functions.get_root_path import get_root_path
from src.views.ErrorWindow import ErrorWindow
from src.views.MainWindow import UIState
from src.views.ConfigView import ConfigView

from src.utils.trenslation_manager.translation_manager import _
from src.utils.trenslation_manager.translation_manager import i18n
from src.views.utils.SystemConfig import SystemConfig
from src.views.utils.lang_code_map import language_to_code


class MainController(QObject):
    error_msg = Signal(str)

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.error_view = None
        self.settings_view = None
        self.model = model

        self.model.config_path = os.path.join(get_root_path(), "config", "config.yml")

        self._worker = None
        self._thread = None

        self.view.file_selected.connect(self.on_file_selected)
        self.view.start_processing.connect(self.on_start_pressed)
        self.view.cancel_processing.connect(self.on_cancel_pressed)
        self.view.open_config.connect(self.open_settings)
        self.view.set_ui_state(UIState.DEFAULT)

        try:
            self.model.curr_lang = language_to_code(SystemConfig.from_yaml(self.model.config_path).language)
        except Exception as e:
            self.show_exeption(e)
            self.model.curr_lang = 'en_US'

        i18n.load_translation(self.model.curr_lang)
        self.view.update_gui_translations()

    def show_exeption(self, exception):
        self.error_view = ErrorWindow(self.view)
        self.error_view.set_error_msg(str(exception))
        self.error_view.show()

    def on_file_selected(self, file_path):
        try:
            qt_image, info_dict = self.model.generate_preview(file_path)
            self.view.update_preview(qt_image, info_dict)
            self.model.video_path = file_path
            self.view.set_ui_state(UIState.DEFAULT)
        except Exception as e:
            self.show_exeption(e)

    def on_start_pressed(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        try:
            self.view.set_ui_state(UIState.PROCESSING)
            video_path = self.model.video_path
            config_path = os.path.join(ROOT_DIR, 'config', 'config.yml')
            if not video_path:
                raise FileNotFoundError(_("No file selected"))

            self._thread = QThread()
            self._worker = video_processor.VideoProcessor(video_path, config_path)
            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._worker.progress.connect(self.view.update_progress)
            self._worker.status.connect(self.view.update_status)

            self._worker.error_status.connect(self.on_processing_error)
            self._worker.cancelled.connect(self.on_processing_cancelled)
            self._worker.finished.connect(self.on_processing_finished)

            # Start!
            self._thread.start()

        except Exception as e:
            self.view.set_ui_state(UIState.ERROR)
            self.show_exeption(e)

    def on_processing_finished(self, results):
        try:
            self.model.results = results
            self.view.display_results(results)
            self.view.set_ui_state(UIState.PROCESSING_FINISHED)
            self._quit_thread()
        except Exception as e:
            self.view.set_ui_state(UIState.ERROR)
            self.show_exeption(e)

    def on_processing_error(self, error):
        self.view.set_ui_state(UIState.ERROR)
        self.show_exeption(error)
        self._quit_thread()

    def on_processing_cancelled(self):
        self.view.set_ui_state(UIState.DEFAULT)
        self.view.update_status(_("Cancelled"))
        self._quit_thread()

    def on_cancel_pressed(self):
        self._worker.cancel()

    def _quit_thread(self):
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(3000)

        if self._worker:
            self._worker.deleteLater()
            self._worker = None

        if self._thread:
            self._thread.deleteLater()
            self._thread = None

    def open_settings(self):
        try:
            self.settings_view = ConfigView(self.model.read_config(), parent=self.view)
            self.settings_view.settings_changed.connect(self._on_settings_saved)
            self.settings_view.exec()
        except Exception as e:
            self.view.set_ui_state(UIState.ERROR)
            self.show_exeption(e)

    def _on_settings_saved(self, new_config: dict, window_persisting : bool):
        try:
            self.model.save_config(new_config)
            new_lang = language_to_code(new_config["system_settings"]["language"])
            if new_lang != self.model.curr_lang:
                self._language_updated(new_lang, window_persisting)

        except Exception as e:
            self.view.set_ui_state(UIState.ERROR)
            self.show_exeption(e)


    def _language_updated(self, new_lang, window_persisting):
        i18n.load_translation(new_lang)
        self.view.update_gui_translations()
        self.model.curr_lang = new_lang

        if window_persisting:
            # Instead of updating each label and every tab we just close and reopen the window
            self.settings_view.close()

            self.settings_view = ConfigView(self.model.read_config(), parent=self.view)
            self.settings_view.settings_changed.connect(self._on_settings_saved)
            self.settings_view.exec()




