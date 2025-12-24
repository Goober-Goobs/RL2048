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

class DQN(nn.Module):
    
    def __init__(self):
        super(DQN,self).__init__()
        self.linear1 = nn.Linear(16*18,400)
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
    
    
    #gets action from policy, epsilon starts large then goes down
    def get_action(self,state):
        sample = random.random()
        #decreases over time, start high then decreases
        eps_threshold = self.EPS_END + (self.EPS_START - self.EPS_END) * math.exp(-1. * self.steps_done / self.EPS_DECAY)
        #random action

        self.steps_done += 1

        if(sample > eps_threshold):
            return random.randint(0,3)
        
        #greedy action
        else:
            output = self.forward(state)
            return torch.argmax(output).item()

    #calculates policy gradient loss based on the reward, state batches, action
    def calculate_loss(self, batch, target_net):
        states, actions, rewards, next_states, dones = batch

        states=torch.FloatTensor(states)
        actions=torch.LongTensor(actions).unsqueeze(1)
        rewards=torch.FloatTensor(rewards)

        next_states=torch.FloatTensor(next_states)
        dones=torch.FloatTensor(dones)

        q_values = self(states).gather(1, actions).squeeze(1)
        with torch.no_grad():
            next_q = target_net(next_states).max(1)[0]
        target = rewards + self.GAMMA * next_q * (1 - dones)
        return F.mse_loss(q_values, target)

    #run through one episode
    def run_episode(self, state):
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
            
            #check if done
            done = state.isGameOver()
            
            #compute reward
            reward = self.compute_reward(curr_board, prev_board, move_score, done)
            
            #save to replay memory
            self.memory.push(state, action, reward, state.board)
            
            #sample from replay memory and train
            if len(self.memory) > self.BATCH_SIZE:

                transitions = self.memory.sample(self.BATCH_SIZE)
                batch = list(zip(*transitions))

                state_batch = torch.cat(batch[0])
                action_batch = torch.cat(batch[1])
                reward_batch = torch.cat(batch[2])
                
                next_state_batch = torch.cat(batch[3])

                #compute loss and backpropagate
                loss = self.calculate_loss(state_batch, action_batch, reward_batch, next_state_batch)
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
                self.optimizer.step()
            else:
                #expand replay memory
                self.run_episode(state, self)

        #update target network
        self.target_net.load_state_dict(self.policy_net.state_dict())

    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
policy_net = DQN().to(device)
target_net = DQN().to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR)
memory = replayMemory(10000)

steps_done = 0

