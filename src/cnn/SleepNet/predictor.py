import torch

from src.cnn.SleepNet.model import SleepNet
from src.cnn.utils import load_model


class SleepNetPredictor:
    def __init__(self, path_to_weights):
        self.model = load_model.load(SleepNet(), path_to_weights)
        self.model.eval()

    @staticmethod
    def __convert_from_numpy_to_tensor(array):
        input_tensor = torch.from_numpy(array).float()

        # Add batch dimension if it's a single image
        if input_tensor.dim() == 2:
            input_tensor = input_tensor.unsqueeze(0).unsqueeze(0)  # (1, 1, H, W)
        elif input_tensor.dim() == 3:  # (H, W, C)
            input_tensor = input_tensor.unsqueeze(0)  # (1, B, H, W)
            input_tensor = input_tensor.permute(1, 0, 2, 3)  # (B, 1, H, W)

        return input_tensor

    def predict_single(self, data):
        tensor = self.__convert_from_numpy_to_tensor(data)

        output = self.model(tensor)
        return output.argmax(dim=1).item()

    def predict_batch(self, batch_data):
        tensor = self.__convert_from_numpy_to_tensor(batch_data)

        outputs = self.model(tensor)
        _, result = outputs.max(dim=1)
        return result.detach().numpy()
