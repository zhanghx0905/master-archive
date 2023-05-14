from copy import deepcopy
from os.path import join as pjoin

import torch.optim as optim
import torch.utils.data as D
import wandb
from torchsummary import summary

from part2_data import Stat, get_dataloaders, load_dataset
from part2_model import Model
from part2_visualize import visualize
from utils import *

DISPLAY_PER_BATCH = 10
BATCH_SIZE = 4
args = parse_args()

wandb.init(project="project1-part2")
set_seed(args["seed"])


def train(net: Model, dataloader: D.DataLoader, optimizer: optim.Optimizer, stat: Stat):
    net.train()
    for features, y_true in dataloader:
        optimizer.zero_grad()
        y_pred = net(features)
        loss = net.loss(y_pred, y_true)

        loss.backward()
        optimizer.step()

        with torch.no_grad():
            lastframe = torch.repeat_interleave(features[:, 4:5, :, :], 5, dim=1)
            loss_lf = net.loss(y_pred, lastframe)
        stat.add(y_pred, y_true, loss, loss_lf, lastframe)
    stat.log()


def test(net: Model, dataloader: D.DataLoader, stat: Stat):
    net.eval()
    with torch.no_grad():
        for features, y_true in dataloader:
            y_pred = net(features)
            loss = net.loss(y_pred, y_true)

            lastframe = torch.repeat_interleave(features[:, 4:5, :, :], 5, dim=1)
            loss_lf = net.loss(y_pred, lastframe)

            stat.add(y_pred, y_true, loss, loss_lf, lastframe)


def train_net():
    training_set, val_set = get_dataloaders(BATCH_SIZE)
    train_stat, val_stat = Stat.create_workers(["train", "val"])
    net = Model(args["bm"])
    summary(net, (5, 32, 32))
    optimizer = optim.Adam(net.parameters(),
                           lr=args['lr'],
                           weight_decay=args["weight_decay"])
    best_loss, best_net = float("inf"), None
    for epoch in range(args["epoch"]):
        print(f"EPOCH {epoch}")
        train(net, training_set, optimizer, train_stat)
        test(net, val_set, val_stat)
        loss = val_stat.log()[0]
        if loss < best_loss:
            best_loss = loss
            best_net = deepcopy(net)
            print(f"Current best epoch is {epoch}")
    net = best_net
    return net


if __name__ == "__main__":
    if args["model_path"] is None:
        net = train_net()
        torch.save(net.state_dict(), pjoin(wandb.run.dir, "model.pth"))
    else:
        net = Model(args["bm"])
        net.load_state_dict(torch.load(args["model_path"]))
    if args["visualize"]:
        _, val_data = load_dataset()
        visualize(net, val_data, pjoin(wandb.run.dir, "img.png"))
