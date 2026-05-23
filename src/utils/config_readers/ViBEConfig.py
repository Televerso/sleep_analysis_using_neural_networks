from dataclasses import dataclass

import yaml


@dataclass()
class ViBEConfig:
    N: int = 20
    R: int = 400
    min: int = 2
    phi: int = 16

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("vibe_motion_detector", {}))