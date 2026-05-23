from dataclasses import dataclass

import yaml


@dataclass()
class BGSubstractorConfig:
    threshold : float = 60
    use_first_or_last_frame_as_the_model : str = 'first'

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data.get("background_substractor", {}))