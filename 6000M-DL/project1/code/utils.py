import argparse
import json
from dataclasses import dataclass, field

import numpy as np
import torch
from torch.cuda import is_available

DEVICE = torch.device("cuda:0" if is_available() else "cpu")
TASK1_TRAINING_DATA_PATH = "./dataset/part1_bballs_training.npz"
TASK1_TEST_DATA_PATH = "./dataset/part1_bballs_test.npz"
TASK2_DATA_PATH = "./dataset/part2_bballs_sequence.npz"


def load_data(path: str, reshape_fn):
    with np.load(path) as f:
        data: np.ndarray = f["data"]
        label: np.ndarray = f["label"]

    return reshape_fn(data), label


def set_seed(seed: int):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


@dataclass
class BaseStat:
    rprefix: str
    loss: list = field(default_factory=list)

    def add(self, loss):
        self.loss.append(loss.item())

    def log(self):
        loss = sum(self.loss) / len(self.loss)
        self.loss.clear()
        return loss

    @classmethod
    def create_workers(cls, names: list[str]):
        return [cls(name) for name in names]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str)
    with open(parser.parse_args().config, "r") as f:
        args = json.load(f)
    return args
