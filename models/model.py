#Creating MNIST model
from torch import nn

class MnistModel(nn.Module):
    def __init__(self):
        super(MnistModel, self).__init__()
        self.cnn_layers = nn.Sequential(
            #CONV1
            nn.Conv2d(1, 6, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            #CONV2
            nn.Conv2d(6, 32, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        self.linear_layers = nn.Sequential(
            nn.Linear(32*5*5, 200),
            nn.ReLU(),
            nn.Linear(200, 80),
            nn.ReLU(),
            nn.Linear(80, 10),
        )
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        return x
