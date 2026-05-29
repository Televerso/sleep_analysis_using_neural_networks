from dataclasses import dataclass

import yaml


@dataclass()
class SystemConfig:
    language: str = "English"

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("system_settings", {}))