import torch
import torch.nn as nn

class SleepNet(nn.Module):
    def __init__(self, ch1: int = 32, ch2:int = 64, ch3:int=128, fc1:int=512, num_classes:int=3, p:float=0.5):
        super().__init__()

        def init_weights(m):
            if isinstance(m, (nn.Conv2d, nn.Linear)):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

        self.features = nn.Sequential(
            # Block 1: 64x64 to 32x32 (in_ch is 1 for the grayscale mask)
            nn.Conv2d(in_channels=1  , out_channels=ch1, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=ch1, out_channels=ch1, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2)),

            # Block 2: 32x32 to 16x16
            nn.Conv2d(in_channels=ch1, out_channels=ch2, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=ch2, out_channels=ch2, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2)),

            # Block 3: 16x16 to 8x8
            nn.Conv2d(in_channels=ch2, out_channels=ch3, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=ch3, out_channels=ch3, kernel_size=(3,3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2)),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(p=p),
            nn.Linear(in_features=ch3*8*8, out_features=fc1),
            nn.ReLU(),
            nn.Linear(in_features=fc1, out_features=num_classes),
            nn.Softmax(dim=1)
        )

        self.apply(init_weights)

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

