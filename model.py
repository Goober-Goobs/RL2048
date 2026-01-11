import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque
from emulator import Emulator
from replayMemory import replayMemory
import random
import math

BATCH_SIZE = 128
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 2500
GAMMA = 0.9 # discount factor
LR = 0.001
STEPS_DONE = 0

class policy(nn.Module):
    
    def __init__(self):
        super(policy,self).__init__()
        self.linear1 = nn.Linear(16,400)
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(400,400)
        self.relu2 = nn.ReLU()
        self.linear3 = nn.Linear(400,4)
        self.softmax = nn.Softmax(dim=1)

    def forward(self,state):
        out = self.linear1(state)
        out = self.relu1(out)
        out = self.linear2(out)
        out = self.relu2(out)
        out = self.linear3(out)
        out = self.softmax(out)
        return out
    
    #computes reward 
    def compute_reward(curr_board, prev_board, move_score, done):
        reward = 0.0

        #good output
        reward += move_score

        #punish if no progress
        reward -= 0.1

        #invalid output
        if move_score == 0 and np.array_equal(prev_board, curr_board):
            reward -= 1.0

        #did not 
        if done:
            max_tile = np.max(prev_board)
            log_tile = np.log2(max_tile) if max_tile > 0 else 1
            reward -= (10 + 2 * log_tile)
        return reward
    
    #gets action from policy
    def get_action(self,state):
        output = self.forward(state)
        return torch.argmax(output).item()
        
    #run through one episode
    def run_episode(self):
        #create new state
        state = Emulator()
        state.startGame()
        STEPS_DONE = 0

        totalRewards = 0
        #run one episode
        while(not state.isGameOver()):
            #get action
            action = self.get_action(state)

            #take action
            prev_board = state.board.copy()
            move_score = state.move(action)
            curr_board = state.board.copy()
            
            #check if done
            done = state.isGameOver()
            
            #compute reward
            output = self.forward(prev_board)
            highestIndex = torch.argmax(output).item()
            output.numpy()

            totalRewards += np.log(output[highestIndex]) * policy.compute_reward(curr_board, prev_board, move_score, False)
            
            #sample from replay memory and train
        
        #game end
        totalRewards += np.log(output[highestIndex]) * policy.compute_reward(curr_board, prev_board, move_score, True)

        #gradient ascent
        optimizer.zero_grad()
        loss = -totalRewards
        loss.backward()
        optimizer.step()


state = Emulator()
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
policy_net = policy().to(device)

optimizer = optim.AdamW(policy_net.parameters(), lr=LR)

policy_net.run_episode()

