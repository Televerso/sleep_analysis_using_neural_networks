import os
from dataclasses import dataclass

import yaml

@dataclass()
class ReaderConfig:
    __ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]

    fps: int = 60
    width: int = 320
    height: int = 240
    rotate: int = 0

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("video_reader", {}))