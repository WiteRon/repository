from torch.utils.data import DataLoader,Dataset
from torchvision.datasets import MNIST
from torchvision.transforms import Compose,ToTensor,Normalize



'''
data_path = r"input path"
class MyDataset(Dataset):
    def __init__(self):
        self.lines = open(data_path).readlines()

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)

my_dataset = MyDataset()
data_loader = DataLoader(dataset=my_dataset,
        batch_size=2, shuffle=True,drop_last=True)

'''

# if __name__ == "__main__":


transform_fn = Compose([
        ToTensor(),
        Normalize((0.137,),(0.3081,))])
dataset = MNIST(
    root="./data",train=True,transform=transform_fn)
data_loader = DataLoader(dataset,batch_size=2,shuffle=True)




for i in enumerate(data_loader):
    print(i)
