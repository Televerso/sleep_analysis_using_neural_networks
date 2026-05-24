import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel,
    QLineEdit, QProgressBar, QScrollArea, QFrame, QVBoxLayout, QTableWidget,
    QSizePolicy, QTableWidgetItem, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QGuiApplication

from src.views.components.hypnogram_widget import HypnogramWidget
from src.views.components.results_panel import ResultsPanel
from enum import Enum

from src.views.utils.is_system_dark_mode import is_system_dark_mode


class UIState(Enum):
    DEFAULT = 0
    PROCESSING = 1
    PROCESSING_FINISHED = 2
    EXPORTING = 3
    ERROR = 4



class MainWindow(QWidget):
    # --- Signals for the controller ---
    file_selected = Signal(str)
    start_processing = Signal()
    cancel_processing = Signal()
    open_config = Signal()

    def __init__(self):
        super().__init__()
        self.ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

        self.setWindowTitle("Sleep Analysis Using Neural Networks")
        self.setMinimumSize(800, 600)

        # --- Main Layout ---
        main_layout = QGridLayout(self)
        # Configure grid stretch factors:
        # Allow Row 2 (the canvas) to take all available extra space.
        main_layout.setRowStretch(1, 1)
        # Allow Column 1 (the input field) to stretch horizontally.
        main_layout.setColumnStretch(1, 1)


        # --- Row 0. File controls. ---
        # Video input label
        main_layout.addWidget(QLabel("Video file:"), 0, 0)

        # Video input field
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Select input video file")
        self.file_path_input.returnPressed.connect(self._on_file_input)
        main_layout.addWidget(self.file_path_input, 0, 1)

        # Video browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self._on_browse_clicked)
        main_layout.addWidget(self.browse_button, 0, 2)


        # --- Row 1. ---
        # --- Row 1: Canvas ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        canvas_layout = QVBoxLayout(content_widget)

        self.hypnogram = HypnogramWidget(is_system_dark_mode())
        canvas_layout.addWidget(self.hypnogram)

        self.results_panel = ResultsPanel()
        canvas_layout.addWidget(self.results_panel)

        canvas_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1, 0, 1, 2)


        # --- Row 1: Preview and action buttons ---
        preview_area = QWidget()
        side_layout = QVBoxLayout(preview_area)

        self.preview_label = QLabel("Preview")
        self.preview_label.setMinimumSize(160, 120)
        self.preview_label.setMaximumSize(160, 120)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid black")
        side_layout.addWidget(self.preview_label, 0, Qt.AlignmentFlag.AlignTop)

        self.preview_param_table = QTableWidget(4, 1)
        self.preview_param_table.horizontalHeader().setVisible(False)
        self.preview_param_table.setVerticalHeaderLabels(('fps','duration','time start','time end'))
        self.preview_param_table.setMaximumWidth(160)
        side_layout.addWidget(self.preview_param_table, 0, Qt.AlignmentFlag.AlignTop)

        # Buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start_clicked)
        side_layout.addWidget(self.start_button, 0, Qt.AlignmentFlag.AlignBottom)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        side_layout.addWidget(self.cancel_button, 0, Qt.AlignmentFlag.AlignBottom)

        self.config_button = QPushButton("Config")
        self.config_button.clicked.connect(self._on_config_clicked)
        side_layout.addWidget(self.config_button, 0, Qt.AlignmentFlag.AlignBottom)

        side_layout.addStretch()
        main_layout.addWidget(preview_area, 1, 2)


        # --- Row 2. progress and export button ---
        self.progress_label = QLabel("Progress")
        main_layout.addWidget(self.progress_label, 2, 0, 2, 2)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar, 3, 0, 3, 2)

        self.export_button = QPushButton("Export")
        self.export_button.setEnabled(False)
        main_layout.addWidget(self.export_button, 3, 2)


    def _on_file_input(self):
        file_path = self.file_path_input.text()
        if file_path and os.path.exists(file_path) and os.path.isfile(file_path):
            self.file_selected.emit(file_path)


    def _on_browse_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   caption="Select video file",
                                                   dir=self.ROOT_DIR,
                                                   filter="Video files (*.mp4 *.mkv *.avi)")
        if file_path:
            self.file_path_input.setText(file_path)
            self.file_selected.emit(file_path)

    def _on_start_clicked(self):
        if self.file_path_input.text():
            self.start_processing.emit()

    def _on_cancel_clicked(self):
        self.progress_label.setText("Cancelling...")
        self.cancel_processing.emit()

    def _on_config_clicked(self):
        self.open_config.emit()

    def update_status(self, status : str):
        self.progress_label.setText(status)

    def update_progress(self, progress : int):
        self.progress_bar.setValue(progress)

    def update_preview(self, qt_image, info_dict):
        pixmap = QPixmap.fromImage(qt_image)
        if pixmap and not pixmap.isNull():
            self.preview_label.setPixmap(pixmap)
            self.preview_param_table.setItem(0, 0, QTableWidgetItem(info_dict['fps']))
            self.preview_param_table.setItem(0, 1, QTableWidgetItem(info_dict['duration']))
            self.preview_param_table.setItem(0, 2, QTableWidgetItem(info_dict['start time']))
            self.preview_param_table.setItem(0, 3, QTableWidgetItem(info_dict['end time']))

    def display_results(self, results):
        self.hypnogram.plot(results["stages"])
        self.results_panel.set_scores(results["scores"])
        self.results_panel.set_parameters(results["parameters"])

    def set_ui_state(self, state: UIState):
        if state == UIState.DEFAULT:
            self.start_button.setEnabled(True)
            self.file_path_input.setEnabled(True)
            self.browse_button.setEnabled(True)
            self.export_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
            self.config_button.setEnabled(True)
            self.progress_label.setStyleSheet("")

        elif state == UIState.PROCESSING:
            self.start_button.setEnabled(False)
            self.file_path_input.setEnabled(False)
            self.browse_button.setEnabled(False)
            self.export_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            self.config_button.setEnabled(False)
            self.progress_label.setStyleSheet("")

        elif state == UIState.PROCESSING_FINISHED:
            self.start_button.setEnabled(True)
            self.file_path_input.setEnabled(True)
            self.browse_button.setEnabled(True)
            self.export_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.config_button.setEnabled(True)
            self.progress_label.setStyleSheet("")

        elif state == UIState.EXPORTING:
            self.start_button.setEnabled(False)
            self.file_path_input.setEnabled(False)
            self.browse_button.setEnabled(False)
            self.export_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
            self.config_button.setEnabled(False)
            self.progress_label.setText("Exporting")
            self.progress_label.setStyleSheet("color: yellow")

        elif state == UIState.ERROR:
            self.start_button.setEnabled(True)
            self.file_path_input.setEnabled(True)
            self.browse_button.setEnabled(True)
            self.export_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
            self.config_button.setEnabled(True)
            self.progress_label.setText("Error")
            self.progress_label.setStyleSheet("color: red")
