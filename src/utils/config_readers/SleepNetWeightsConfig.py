from dataclasses import dataclass

import yaml


@dataclass()
class SleepNetWeightsConfig:
    path_to_weights : str

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("sleep_net_weights", {}))