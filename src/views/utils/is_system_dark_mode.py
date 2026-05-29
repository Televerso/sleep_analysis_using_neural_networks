from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication


def is_system_dark_mode():
    """Returns True if the OS is using dark mode."""
    try:
        # Available in Qt 6.5+
        return QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark
    except AttributeError:
        # Fallback for older Qt versions
        return False