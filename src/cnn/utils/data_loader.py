import os

from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split

def make_loaders(path : str, batch_size: int = 32, val_to_train_ratio : float = 0.05):
    if not os.path.exists(path):
        raise FileNotFoundError
    if not os.path.isdir(path):
        raise NotADirectoryError

    if not os.path.exists(os.path.join(path, 'Test' )):
        raise FileNotFoundError
    if not os.path.exists(os.path.join(path, 'Train')):
        raise FileNotFoundError

    if val_to_train_ratio < 0 or val_to_train_ratio > 1:
        raise ValueError


    # Define transforms
    train_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),  # Converts to [0, 1] float tensor
    ])
    test_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),  # Converts to [0, 1] float tensor
    ])

    # Load dataset
    full_train_dataset = datasets.ImageFolder(
        root=os.path.join(path, 'Train'),
        transform=train_transform
    )
    test_dataset = datasets.ImageFolder(
        root=os.path.join(path, 'Test'),
        transform=test_transform
    )

    # Split training dataset
    total_size = len(full_train_dataset)
    val_size = int(val_to_train_ratio * total_size)
    train_size = total_size - val_size
    train_dataset, val_dataset = random_split(
        full_train_dataset,
        [train_size, val_size]
    )

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return {"train_loader" : train_loader, "val_loader": val_loader,"test_loader": test_loader}