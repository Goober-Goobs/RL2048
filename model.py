import numpy as np
import torch.nn as nn
import torch.optim as optim
from collctions import deque
import random

class DQN(nn.Module):
    def __init__(self):
        super(DQN,self).__init__()
        self.linear1 = nn.linear(16*18,400)
        self.relu1 = nn.relu()
        self.linear2 = nn.linear(400,400)
        self.relu2 = nn.relu()
        self.linear3 = nn.linear(400,4)
        self.softmax = nn.softmax(dim=1)

    def forward(self,state):
        out = self.linear1(state)
        out = self.relu1(out)
        out = self.linear2(out)
        out = self.relu2(out)
        out = self.linear3(out)
        out = self.softmax(out)
        return out

        

