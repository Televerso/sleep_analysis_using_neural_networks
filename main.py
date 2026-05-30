import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.controllers.MainController import MainController
from src.models.MainModel import MainModel
from src.utils.file_functions.get_root_path import get_root_path
from src.views.MainWindow import MainWindow
from src.utils.trenslation_manager.translation_manager import i18n

def main(*args, **kwargs):
    app = QApplication(sys.argv)

    icon_path = os.path.join(get_root_path(), "resources", "icons", "sleep.ico")
    app.setWindowIcon(QIcon(icon_path))

    view = MainWindow()
    model = MainModel()
    controller = MainController(view, model)
    view.show()

    sys.exit(app.exec())
    pass

if __name__ == '__main__':
    main()
