import numpy as np
import torch.nn as nn
import torch.optim as optim
from collctions import deque
import random
import emulator

class DQN(nn.Module):
    def __init__(self):
        super(DQN,self).__init__()
        self.linear1 = nn.linear(16*18,400)
        self.relu1 = nn.relu()
        self.linear2 = nn.linear(400,400)
        self.relu2 = nn.relu()
        self.linear3 = nn.linear(400,4)
        self.argmax = nn.argmax(dim=1)

    def forward(self,state):
        out = self.linear1(state)
        out = self.relu1(out)
        out = self.linear2(out)
        out = self.relu2(out)
        out = self.linear3(out)
        out = self.argmax(out)
        return out



    def compute_reward(prev_board, move_score, done):
        reward = 0.0

        #good boy (merge reward)
        reward += move_score

        #make progress or you get the belt
        reward -= 0.1

        #no time waste
        if move_score == 0 and np.array_equal(prev_board, arr):
            reward -= 1.0

        #Failure, belt time :3
        if done:
            max_tile = np.max(prev_board)
            log_tile = np.log2(max_tile) if max_tile > 0 else 1
            reward -= (10 + 2 * log_tile)
        return reward
    

    #calculates loss based on the reward
    def calculate_loss(self, reward):

    
    #update the model based on the loss
    def update_model(self, loss):
        #convert reward to loss




    #run through one episode
    def run_episode(state, self):
        #create new state
        state = Emulator()
        state.startGame()
    
        

