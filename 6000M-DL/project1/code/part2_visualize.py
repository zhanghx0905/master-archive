import numpy as np
import torch
import matplotlib.pyplot as plt

from part2_model import Model


def visualize(net: Model, dataset, path: str):
    x, y_true = dataset[0]
    with torch.no_grad():
        y_pred = net(x)
    y_true = y_true.cpu().numpy()
    y_pred = y_pred.cpu().detach().numpy()
    draw_sample(y_true, y_pred, path)


def draw_sample(Yt: np.ndarray, Yp: np.ndarray, path: str):
    nfigures = Yt.shape[0]
    for i in range(1, nfigures + 1):
        ax = plt.subplot(2, nfigures, i)
        ax.imshow(Yt[i - 1])
    for i in range(nfigures + 1, 2 * nfigures + 1):
        ax = plt.subplot(2, nfigures, i)
        ax.imshow(Yp[i - 1 - nfigures])
    plt.savefig(path)
