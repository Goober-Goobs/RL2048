import numpy as np
import torch.nn as nn
import torch.optim as optim
from collections import deque
from emulator import Emulator
from replayMemory import ReplayMemory

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


    #computes reward a
    def compute_reward(curr_board, prev_board, move_score, done):
        reward = 0.0

        #good boy (merge reward)
        reward += move_score

        #make progress or you get the belt
        reward -= 0.1

        #no time waste
        if move_score == 0 and np.array_equal(prev_board, curr_board):
            reward -= 1.0

        #Failure, belt time :3
        if done:
            max_tile = np.max(prev_board)
            log_tile = np.log2(max_tile) if max_tile > 0 else 1
            reward -= (10 + 2 * log_tile)
        return reward
    

    '''
    very much wip help D:
    '''
    
    def get_action(self, state):
        #get action from model
        output = self.forward(state)
        return output

    #calculates loss based on the reward
    def calculate_loss(self, reward):
        pass
    
    #update the model based on the loss
    def update_model(self, reward):
        loss = calculate_loss(self,reward)
        #backprop

    #run through one episode
    def run_episode(state, self):
        #create new state
        state = Emulator()
        state.startGame()

        while(not state.isGameOver()):
            #get action
            action = self.get_action(state)
            #take action
            prev_board = state.board.copy()
            move_score = state.move(action)
            curr_board = state.board.copy()
            done = state.isGameOver()
            #compute reward
            reward = self.compute_reward(curr_board, prev_board, move_score, done)
            #update model (backpropagate)
            self.update_model(reward)
            #save to replay memory

    
        

