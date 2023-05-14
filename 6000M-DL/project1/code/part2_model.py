import torch.nn as nn

from utils import DEVICE


class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, bm: bool = False) -> None:
        super().__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels) if bm else nn.Identity(),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels) if bm else nn.Identity(),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.layer(x)


class TransConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, bm: bool = False) -> None:
        super().__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels) if bm else nn.Identity(),
            nn.ReLU(),
            nn.ConvTranspose2d(out_channels, out_channels, 2, stride=2),
            nn.BatchNorm2d(out_channels) if bm else nn.Identity(),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.layer(x)


class Encoder(nn.Module):
    def __init__(self, in_channels: int, bm: bool = False) -> None:
        super().__init__()
        self.conv1 = ConvBlock(in_channels, 32, bm)
        self.conv2 = ConvBlock(32, 64, bm)
        self.conv3 = ConvBlock(64, 128, bm)
        self.conv4 = ConvBlock(128, 128, bm)
        self.max_pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        skip1 = self.conv1(x)
        skip2 = self.conv2(self.max_pool(skip1))
        skip3 = self.conv3(self.max_pool(skip2))
        return skip1, skip2, skip3, self.max_pool(skip3)


class Decoder(nn.Module):
    def __init__(self, out_channels: int, bm: bool = False) -> None:
        super().__init__()
        self.conv1 = TransConvBlock(128, 128, bm)
        self.conv2 = TransConvBlock(128, 64, bm)
        self.conv3 = TransConvBlock(64, 32, bm)
        self.conv_out = ConvBlock(32, out_channels)

    def forward(self, skip1, skip2, skip3, x):
        x = self.conv1(x) + skip3
        x = self.conv2(x) + skip2
        x = self.conv3(x) + skip1
        x = self.conv_out(x)
        return x


class Model(nn.Module):
    def __init__(self, bm: bool = False) -> None:
        super().__init__()
        self.encoder = Encoder(5, bm)
        self.decoder = Decoder(5, bm)
        self.loss = nn.MSELoss()
        self.to(DEVICE)

    def forward(self, x):
        return self.decoder(*self.encoder(x))
