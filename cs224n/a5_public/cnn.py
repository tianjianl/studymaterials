#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CS224N 2019-20: Homework 5
"""

import torch
import torch.nn as nn

class CNN(nn.Module):
    # Remember to delete the above 'pass' after your implementation
    ### YOUR CODE HERE for part 1g
    def __init__(self, c_in, c_out, k, pad):
        super(CNN, self).__init__()
        self.conv = nn.Conv1d(c_in, c_out, k, padding=pad)
    
    def forward(self, x_reshaped):
        x_conv = self.conv(x_reshaped)
        x_conv = nn.functional.relu(x_conv)
        x_conv_out = torch.max(x_conv, -1).values
        return x_conv_out

    ### END YOUR CODE

