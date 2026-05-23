from dataclasses import dataclass

import yaml


@dataclass()
class SleepAnalyzerConfig:
    epoch_len: int = 30
    movement_threshold: float = 0.01
    wake_threshold: float = 0.1

    Am: float = 8.5
    Ap: float = 8.5
    Aw: float = 2
    alpha: float = 1
    beta: float = 0.01
    gamma: float = 0.5

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("sleep_analyzer", {}))