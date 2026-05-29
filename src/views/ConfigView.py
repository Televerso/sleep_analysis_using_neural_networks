from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QWidget, QSpinBox, QDoubleSpinBox,
    QComboBox, QLineEdit, QPushButton, QFileDialog,
    QDialogButtonBox, QCheckBox, QGroupBox, QLabel, QButtonGroup, QRadioButton
)
from PySide6.QtCore import Qt, Signal

from src.utils.file_functions.get_root_path import get_root_path

from src.utils.trenslation_manager.translation_manager import _
from src.views.utils.lang_code_map import language_to_id, id_to_language


class ConfigView(QDialog):
    settings_changed = Signal(dict)

    def __init__(self, curr_config : dict , parent=None):
        super().__init__(parent)

        self.setWindowTitle(_("Settings"))
        self.setMinimumSize(600, 400)
        self._config = curr_config.copy()

        # Building the layout
        main_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # --- Video processing ---
        video_tab = QWidget()
        video_layout = QFormLayout(video_tab)

        self.fps = QDoubleSpinBox()
        self.fps.setRange(0.1, 60)
        self.fps.setSingleStep(0.1)
        self.fps.setToolTip(_("Target fps to process"))
        video_layout.addRow(_('FPS: '), self.fps)

        self.resize_width = QSpinBox()
        self.resize_width.setRange(60, 360)
        self.resize_width.setSingleStep(1)
        self.resize_width.setToolTip(_("Width of the processed video"))
        video_layout.addRow(_('Width: '), self.resize_width)

        self.resize_height = QSpinBox()
        self.resize_height.setRange(40, 240)
        self.resize_height.setSingleStep(1)
        self.resize_height.setToolTip(_("Height of the processed video"))
        video_layout.addRow(_('Height: '), self.resize_height)


        # Create a container widget for the radio buttons
        rotation_container = QWidget()

        rotation_layout = QHBoxLayout(rotation_container)

        self.rotate_video = QButtonGroup(rotation_container)
        rotate_0 = QRadioButton('0')
        self.rotate_video.addButton(rotate_0, id=0)
        rotate_90 = QRadioButton('90')
        self.rotate_video.addButton(rotate_90, id=1)
        rotate_180 = QRadioButton('180')
        self.rotate_video.addButton(rotate_180, id=2)
        rotate_270 = QRadioButton('270')
        self.rotate_video.addButton(rotate_270, id=3)

        # Add radio buttons to the horizontal layout
        rotation_layout.addWidget(rotate_0)
        rotation_layout.addWidget(rotate_90)
        rotation_layout.addWidget(rotate_180)
        rotation_layout.addWidget(rotate_270)

        # Add the container to the form
        video_layout.addRow(_('Rotate: '), rotation_container)

        self.tab_widget.addTab(video_tab, _("Video Processing"))

        # --- Motion Detection ---
        motion_tab = QWidget()
        motion_layout = QFormLayout(motion_tab)

        self.vibe_n = QSpinBox()
        self.vibe_n.setRange(1, 32)
        self.vibe_n.setSingleStep(1)
        self.vibe_n.setToolTip(_("Number of samples per pixel"))
        motion_layout.addRow(_('ViBE Samples (N): '), self.vibe_n)

        self.vibe_r = QSpinBox()
        self.vibe_r.setRange(1, 100)
        self.vibe_r.setSingleStep(1)
        self.vibe_r.setToolTip(_("Radius threshold for pixel matching"))
        motion_layout.addRow(_('ViBE Radius (R): '), self.vibe_r)

        self.vibe_min = QSpinBox()
        self.vibe_min.setRange(1, 10)
        self.vibe_min.setSingleStep(1)
        self.vibe_min.setToolTip(_("Minimum matches for background classification"))
        motion_layout.addRow(_('ViBE Min (#min): '), self.vibe_min)

        self.vibe_phi = QSpinBox()
        self.vibe_phi.setRange(1, 100)
        self.vibe_phi.setSingleStep(1)
        self.vibe_phi.setToolTip(_("1/phi chance to update the background"))
        motion_layout.addRow(_('ViBE Phi (phi): '), self.vibe_phi)

        self.tab_widget.addTab(motion_tab, _('Motion Processing'))

        # --- Background substraction ---
        bgs_tab = QWidget()
        bgs_layout = QFormLayout(bgs_tab)

        self.bgs_threshold = QSpinBox()
        self.bgs_threshold.setRange(0, 255)
        self.bgs_threshold.setSingleStep(1)
        self.bgs_threshold.setToolTip(_("Threshold for background classification"))
        bgs_layout.addRow(_('Background Threshold: '), self.bgs_threshold)

        self.tab_widget.addTab(bgs_tab, _('Background Processing'))

        # --- SleepNet weights ---
        cnn_tab = QWidget()
        cnn_layout = QFormLayout(cnn_tab)

        self.model_weights = QLineEdit()
        browse_button = QPushButton(_("Browse"))
        browse_button.clicked.connect(self._browse_weights)

        weights_container = QWidget()
        weights_layout = QHBoxLayout(weights_container)
        weights_layout.addWidget(QLabel(_('Model weights: ')))
        weights_layout.addWidget(self.model_weights)
        weights_layout.addWidget(browse_button)
        cnn_layout.addRow(weights_container)

        self.tab_widget.addTab(cnn_tab, _('CNN layout'))

        # --- Sleep analyzer ---
        sleep_analyzer_tab = QWidget()
        sleep_analyzer_layout = QFormLayout(sleep_analyzer_tab)

        self.epoch_len = QSpinBox()
        self.epoch_len.setRange(1, 120)
        self.epoch_len.setSingleStep(1)
        self.epoch_len.setToolTip(_("Length of the epoch"))
        sleep_analyzer_layout.addRow(_('Epoch Length: '), self.epoch_len)

        self.sleep_movement_threshold = QDoubleSpinBox()
        self.sleep_movement_threshold.setRange(0.005, 1)
        self.sleep_movement_threshold.setSingleStep(0.005)
        self.sleep_movement_threshold.setToolTip(_("Threshold for detecting the sleep movement"))
        sleep_analyzer_layout.addRow(_('Sleep Movement Threshold: '), self.sleep_movement_threshold)

        self.awake_threshold = QDoubleSpinBox()
        self.awake_threshold.setRange(0.005, 1)
        self.awake_threshold.setSingleStep(0.005)
        self.awake_threshold.setToolTip(_("Threshold for detecting the wake state"))
        sleep_analyzer_layout.addRow(_('Awake Threshold: '), self.awake_threshold)

        self.sleep_Am = QDoubleSpinBox()
        self.sleep_Am.setRange(1, 12)
        self.sleep_Am.setSingleStep(0.5)
        self.sleep_Am.setToolTip(_("Optimal sleep duration"))
        sleep_analyzer_layout.addRow(_('Sleep Am: '), self.sleep_Am)

        self.sleep_Ap = QDoubleSpinBox()
        self.sleep_Ap.setRange(1, 12)
        self.sleep_Ap.setSingleStep(0.5)
        self.sleep_Ap.setToolTip(_("Personolized sleep duration"))
        sleep_analyzer_layout.addRow(_('Sleep Ap: '), self.sleep_Ap)

        self.sleep_Aw = QSpinBox()
        self.sleep_Aw.setRange(0, 12)
        self.sleep_Aw.setSingleStep(1)
        self.sleep_Aw.setToolTip(_("Optimal number ow awakings"))
        sleep_analyzer_layout.addRow(_('Sleep Aw: '), self.sleep_Aw)

        self.sleep_alpha = QDoubleSpinBox()
        self.sleep_alpha.setRange(0, 1)
        self.sleep_alpha.setSingleStep(0.01)
        self.sleep_alpha.setToolTip(_("Alpha coefficient"))
        sleep_analyzer_layout.addRow(_('Sleep Alpha: '), self.sleep_alpha)

        self.sleep_beta = QDoubleSpinBox()
        self.sleep_beta.setRange(0, 1)
        self.sleep_beta.setSingleStep(0.01)
        self.sleep_beta.setToolTip(_("Beta coefficient"))
        sleep_analyzer_layout.addRow(_('Sleep Beta: '), self.sleep_beta)

        self.sleep_gamma = QDoubleSpinBox()
        self.sleep_gamma.setRange(0, 1)
        self.sleep_gamma.setSingleStep(0.01)
        self.sleep_gamma.setToolTip(_("Gamma coefficient"))
        sleep_analyzer_layout.addRow(_('Sleep Gamma: '), self.sleep_gamma)

        self.tab_widget.addTab(sleep_analyzer_tab, _('Sleep Analysis'))


        # --- System settings ---
        system_settings_tab = QWidget()
        system_settings_layout = QFormLayout(system_settings_tab)

        self.lang_locale = QComboBox()
        self.lang_locale.addItem(_('English'))
        self.lang_locale.addItem(_('Russian'))
        self.lang_locale.setToolTip(_("Language selector"))
        system_settings_layout.addRow(_('Language selector: '), self.lang_locale)

        self.tab_widget.addTab(system_settings_tab, _('System Settings'))


        # --- Dialog Buttons ---

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self._on_save)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText(_("Ok"))
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(_("Cancel"))
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._on_apply)
        button_box.button(QDialogButtonBox.StandardButton.Apply).setText(_("Apply"))

        main_layout.addWidget(button_box)

        self._load_curr_values()

        self.setLayout(main_layout)


    def _load_curr_values(self):
        cfg = self._config

        self.fps.setValue(cfg.get("video_reader",{}).get("fps", 1))
        self.resize_width.setValue(cfg.get("video_reader",{}).get("width", 160))
        self.resize_height.setValue(cfg.get("video_reader",{}).get("height", 120))
        self.rotate_video.button(cfg.get("video_reader",{}).get("rotate", 0)).click()

        self.vibe_n.setValue(cfg.get("vibe_motion_detector",{}).get("N", 20))
        self.vibe_r.setValue(cfg.get("vibe_motion_detector",{}).get("R", 40))
        self.vibe_min.setValue(cfg.get("vibe_motion_detector",{}).get("min", 2))
        self.vibe_phi.setValue(cfg.get("vibe_motion_detector",{}).get("phi", 16))

        self.bgs_threshold.setValue(cfg.get("background_substractor",{}).get("threshold", 60))

        self.model_weights.setText(cfg.get("sleep_net_weights",{}).get("path_to_weights", None))

        self.epoch_len.setValue(cfg.get("sleep_analyzer",{}).get("epoch_len", 30))
        self.sleep_movement_threshold.setValue(cfg.get("sleep_analyzer",{}).get("movement_threshold", 0.01))
        self.awake_threshold.setValue(cfg.get("sleep_analyzer",{}).get("wake_threshold", 0.1))

        self.sleep_Am.setValue(cfg.get("sleep_analyzer",{}).get("Am", 8.5))
        self.sleep_Ap.setValue(cfg.get("sleep_analyzer",{}).get("Ap", 8.5))
        self.sleep_Aw.setValue(cfg.get("sleep_analyzer",{}).get("Aw", 2))

        self.sleep_alpha.setValue(cfg.get("sleep_analyzer",{}).get("alpha", 1))
        self.sleep_beta.setValue(cfg.get("sleep_analyzer",{}).get("beta", 0.01))
        self.sleep_gamma.setValue(cfg.get("sleep_analyzer",{}).get("gamma", 0.5))

        curr_language = cfg.get("system_settings",{}).get("language","English")
        self.lang_locale.setCurrentIndex(language_to_id(curr_language))


    def _collect_values(self):
        cfg = dict()

        cfg["video_reader"] = dict()
        cfg["video_reader"]["fps"] = self.fps.value()
        cfg["video_reader"]["width"] = self.resize_width.value()
        cfg["video_reader"]["height"] = self.resize_height.value()
        cfg["video_reader"]["rotate"] = self.rotate_video.checkedId() if self.rotate_video.checkedId() != -1 else 0

        cfg["vibe_motion_detector"] = dict()
        cfg["vibe_motion_detector"]["N"] = self.vibe_n.value()
        cfg["vibe_motion_detector"]["R"] = self.vibe_r.value()
        cfg["vibe_motion_detector"]["min"] = self.vibe_min.value()
        cfg["vibe_motion_detector"]["phi"] = self.vibe_phi.value()

        cfg["background_substractor"] = dict()
        cfg["background_substractor"]["threshold"] = self.bgs_threshold.value()

        cfg["sleep_net_weights"] = dict()
        cfg["sleep_net_weights"]["path_to_weights"] = self.model_weights.text()

        cfg["sleep_analyzer"] = dict()
        cfg["sleep_analyzer"]["epoch_len"] = self.epoch_len.value()
        cfg["sleep_analyzer"]["movement_threshold"] = self.sleep_movement_threshold.value()
        cfg["sleep_analyzer"]["wake_threshold"] = self.awake_threshold.value()

        cfg["sleep_analyzer"]["Am"] = self.sleep_Am.value()
        cfg["sleep_analyzer"]["Ap"] = self.sleep_Ap.value()
        cfg["sleep_analyzer"]["Aw"] = self.sleep_Aw.value()

        cfg["sleep_analyzer"]["alpha"] = self.sleep_alpha.value()
        cfg["sleep_analyzer"]["beta"] = self.sleep_beta.value()
        cfg["sleep_analyzer"]["gamma"] = self.sleep_gamma.value()


        cfg["system_settings"] = dict()
        cfg["system_settings"]["language"] = id_to_language(self.lang_locale.currentIndex())

        return cfg

    def _on_save(self):
        new_config = self._collect_values()
        self.settings_changed.emit(new_config)
        self.accept()

    def _on_apply(self):
        new_config = self._collect_values()
        self.settings_changed.emit(new_config)

    def _browse_weights(self):
        file_path, tmp = QFileDialog.getOpenFileName(self, _('Open weights file'), dir=get_root_path(),
                                                   filter="PyTorch Weights (*.pth);;All Files (*)")
        if file_path:
            self.model_weights.setText(file_path)








