from dataclasses import dataclass, field
from functools import partial
from os.path import join as pjoin

import torch.nn as nn
import torch.optim as optim
import torch.utils.data as D
from sklearn.metrics import accuracy_score, classification_report
from torchsummary import summary

import wandb
from utils import *

wandb.init(project="project1-part1")


DISPLAY_PER_BATCH = 10
args = parse_args()
set_seed(args["seed"])


class Dataset(D.Dataset):
    def __init__(self, data: np.ndarray, label: np.ndarray) -> None:
        super().__init__()
        self.data = torch.FloatTensor(data).to(DEVICE)
        self.label = torch.LongTensor(label).to(DEVICE)
        self.label -= 1

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index], self.label[index]


class Model(nn.Module):
    def __init__(self, bm=False) -> None:
        super().__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.BatchNorm2d(16) if bm else nn.Identity(),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.BatchNorm2d(32) if bm else nn.Identity(),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 16, 3, padding=1),
            nn.BatchNorm2d(16) if bm else nn.Identity(),
            nn.ReLU(),
            nn.Conv2d(16, 16, 3, padding=1),
            nn.BatchNorm2d(16) if bm else nn.Identity(),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.ReLU(),
            nn.Linear(64, 3),
        )
        self.loss = nn.CrossEntropyLoss()
        self.to(DEVICE)

    def forward(self, x):
        y = self.layer(x)
        return y


@dataclass
class Stat(BaseStat):
    labels: list = field(default_factory=list)
    pred_labels: list = field(default_factory=list)

    def add(self, pred, gold_labels, loss):
        super().add(loss)
        gold_labels = gold_labels.cpu().numpy()
        pred = pred.cpu().detach().numpy()
        pred_labels = np.argmax(pred, axis=1)

        self.labels.extend(gold_labels)
        self.pred_labels.extend(pred_labels)

    def log(self):
        loss = super().log()
        acc = accuracy_score(self.labels, self.pred_labels)
        self.labels = []
        self.pred_labels = []
        wandb.log(
            {
                f"{self.rprefix}_loss": loss,
                f"{self.rprefix}_acc": acc,
            }
        )
        return loss, acc


def train(net: Model, dataloader: D.DataLoader, optimizer: optim.Optimizer, stat: Stat):
    net.train()
    for i, (features, y_true) in enumerate(dataloader):
        optimizer.zero_grad()
        y_pred = net(features)
        loss = net.loss(y_pred, y_true)

        loss.backward()
        optimizer.step()
        stat.add(y_pred, y_true, loss)
        # if (i + 1) % DISPLAY_PER_BATCH == 0:
    stat.log()


def test(net: Model, dataloader: D.DataLoader, stat: Stat):
    net.eval()
    with torch.no_grad():
        for features, y_true in dataloader:
            y_pred = net(features)
            loss = net.loss(y_pred, y_true)
            stat.add(y_pred, y_true, loss)


def load_dataset():
    from utils import load_data

    load_data = partial(load_data, reshape_fn=lambda data: data.reshape(-1, 1, 32, 32))
    training_data = Dataset(*load_data(TASK1_TRAINING_DATA_PATH))
    training_data, val_data = D.random_split(training_data, [0.8, 0.2])
    training_set = D.DataLoader(training_data, 4, shuffle=True)
    val_set = D.DataLoader(val_data, 4)

    test_data = Dataset(*load_data(TASK1_TEST_DATA_PATH))
    test_set = D.DataLoader(test_data, 4)
    return training_set, val_set, test_set


def task1():
    training_set, val_set, test_set = load_dataset()
    train_stat, val_stat, test_stat = Stat.create_workers(["train", "val", "test"])
    net = Model(args["bm"])
    summary(net, (1, 32, 32))
    optimizer = optim.Adam(net.parameters(), weight_decay=args["weight_decay"])
    for epoch in range(args["epoch"]):
        print(f"EPOCH {epoch}")
        train(net, training_set, optimizer, train_stat)
        test(net, val_set, val_stat)
        val_stat.log()
    test(net, test_set, test_stat)
    print(
        classification_report(
            test_stat.labels, test_stat.pred_labels, target_names=["1", "2", "3"]
        )
    )
    loss, acc = test_stat.log()
    torch.save(net.state_dict(), pjoin(wandb.run.dir, "model.pth"))
    return loss, acc


if __name__ == "__main__":
    task1()
