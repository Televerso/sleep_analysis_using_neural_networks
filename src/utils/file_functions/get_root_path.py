import os
import sys
from pathlib import Path

def get_root_path():
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = os.path.split(os.environ['VIRTUAL_ENV'])[0]

    return base_path