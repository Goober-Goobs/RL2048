from emulator.py import Emulator
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from model import policy

#batch size == num of episodes
BATCH_SIZE = 1000
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 2500

#

#training loop
def train():
    state = Emulator()
    policy_net = policy()
    for i in range(BATCH_SIZE):
        state.reset()
        state.startGame()
        total_score = 0
        while(not state.isGameOver()):
            #get current board state
            curr_board = torch.FloatTensor(state.arr.flatten()).unsqueeze(0)

            #select action
            action_tensor = policy_net.get_action(curr_board)

            #action is softmax output (tensor)
            #convert action_tensor to actual action (0-3)

            action = torch.argmax(action_tensor)
            score_earned = state.move(action)


            


