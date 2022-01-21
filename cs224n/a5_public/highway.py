#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CS224N 2019-20: Homework 5
"""

import torch
import torch.nn as nn

class Highway(nn.Module):
    # Remember to delete the above 'pass' after your implementation
    ### YOUR CODE HERE for part 1f
    def __init__(self, hidden_size):
        super(Highway, self).__init__()
        self.proj_linear = nn.Linear(hidden_size, hidden_size, bias=True)
        self.gate_linear = nn.Linear(hidden_size, hidden_size, bias=True)
        
    def forward(self, x_conv_out):
        x_proj = nn.functional.relu(self.proj_linear(x_conv_out))
        x_gate = torch.sigmoid(self.gate_linear(x_conv_out))
        x_highway = x_gate * x_proj + (1 - x_gate) * x_conv_out
        
        return x_highway


    ### END YOUR CODE

