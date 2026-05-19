import torch

def load(model:torch.nn.Module, filepath: str):
    checkpoint = torch.load(filepath)
    model.load_state_dict(checkpoint['model_state_dict'])
    return model