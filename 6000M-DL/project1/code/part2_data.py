from dataclasses import dataclass, field

import wandb
import torch.utils.data as D
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

from utils import *


class Dataset(D.Dataset):
    def __init__(self, data: np.ndarray):
        super().__init__()
        X = data[:, :5, :]
        Y = data[:, 5:, :]
        self.X = torch.FloatTensor(X).to(DEVICE)
        self.Y = torch.FloatTensor(Y).to(DEVICE)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return self.X[index], self.Y[index]


def load_dataset():
    data, _ = load_data(TASK2_DATA_PATH, lambda data: data.reshape(-1, 10, 32, 32))
    dataset = Dataset(data)
    return D.random_split(dataset, [0.8, 0.2])


def get_dataloaders(batch_size: int):
    training_data, val_data = load_dataset()
    training_set = D.DataLoader(training_data, batch_size, shuffle=True)
    val_set = D.DataLoader(val_data, batch_size)
    return training_set, val_set


@dataclass
class Stat(BaseStat):
    true_ys: list = field(default_factory=list)
    pred_ys: list = field(default_factory=list)
    loss_lf: list = field(default_factory=list)
    lf: list = field(default_factory=list)

    def add(self, pred_y, true_y, loss, loss_lf, lf):
        true_y = true_y.cpu().numpy()
        pred_y = pred_y.cpu().detach().numpy()
        lf = lf.cpu().numpy()
        self.loss_lf.append(loss_lf.item())
        super().add(loss)
        self.true_ys.extend(list(true_y.reshape(-1, 32, 32)))
        self.pred_ys.extend(list(pred_y.reshape(-1, 32, 32)))
        self.lf.extend(list(lf.reshape(-1, 32, 32)))

    def cal_ssim_psnr(self, x, y):
        ssim, psnr = [], []
        for true_y, pred_y in zip(x, y):
            ssim.append(structural_similarity(true_y, pred_y, data_range=1))
            psnr.append(peak_signal_noise_ratio(true_y, pred_y, data_range=1))
        ssim = np.mean(ssim)
        psnr = np.mean(psnr)
        return ssim, psnr

    def log(self):
        loss = super().log()
        loss_lf = sum(self.loss_lf) / len(self.loss_lf)
        self.loss_lf.clear()

        ssim, psnr = self.cal_ssim_psnr(self.true_ys, self.pred_ys)
        ssim_lf, psnr_lf = self.cal_ssim_psnr(self.lf, self.pred_ys)
        self.true_ys.clear()
        self.pred_ys.clear()
        self.lf.clear()

        logs = {
            f"{self.rprefix}_loss": loss,
            f"{self.rprefix}_ssim": ssim,
            f"{self.rprefix}_psnr": psnr,
            f"{self.rprefix}_loss_lf": loss_lf,
            f"{self.rprefix}_ssim_lf": ssim_lf,
            f"{self.rprefix}_psnr_lf": psnr_lf,
        }
        wandb.log(logs)
        return list(logs.values())
