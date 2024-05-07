import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import SGD,Adam
import numpy as np
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader,Dataset
import torchvision
from torchvision.datasets import MNIST
from torchvision import transforms
from torchvision.transforms import Compose,ToTensor,Normalize
import os


BATCH_SIZE = 128
TEST_BATCH_SIZZE = 1000


def get_dataloader(train=True,batch_size = BATCH_SIZE):
    transform_fn = Compose([
            ToTensor(),
            Normalize((0.137,),(0.3081,))])
    dataset = MNIST(
        root="./data",train=train,download=False,
        transform=transform_fn)
    data_loader = DataLoader(dataset=dataset,
                             batch_size=batch_size,shuffle=True)
    return data_loader


class MnistModel(nn.Module):
    def __init__(self):
        super(MnistModel, self).__init__()
        self.fc1 = nn.Linear(1*28*28,28)
        self.fc2 = nn.Linear(28,10)

    def forward(self,input):
        x = input.view([input.size(0),1*28*28])
        x = self.fc1(x)
        x = F.relu(x)
        out = self.fc2(x)
        return F.log_softmax(out,dim=-1)


def train(epoch):
    data_loader = get_dataloader()
    for idx,(input,target) in enumerate(data_loader):
        optimizer.zero_grad()
        output = model(input)
        loss = F.nll_loss(output,target)
        loss.backward()
        optimizer.step()
        if idx % 100 == 0:
            print(epoch,idx,loss.item())

        # save function
        if idx % 100 == 0:
            torch.save(model.state_dict(),"./model/model.pkl")
            torch.save(optimizer.state_dict(), "./model/optimizer.pkl")


def test():
    loss_list = []
    acc_list = []
    test_dataloader = get_dataloader(train=False)
    for idx,(input,target) in enumerate(test_dataloader):
        with torch.no_grad():
            output = model(input)
            cur_loss = F.nll_loss(output,target)
            loss_list.append(cur_loss)
            pred = output.max(dim=-1)[-1]
            cur_acc = pred.eq(target).float().mean()
            acc_list.append(cur_acc)
    print("acc and loss:",np.mean(acc_list),np.mean(loss_list))


if __name__ == "__main__":
    model = MnistModel()
    optimizer = Adam(model.parameters(), lr=0.001)
    if os.path.exists("./model/model.pkl"):
        model.load_state_dict(torch.load("./model/model.pkl"))
        optimizer.load_state_dict(torch.load("./model/optimizer.pkl"))

    # for i in range(3):
    #     train(i)
    test()