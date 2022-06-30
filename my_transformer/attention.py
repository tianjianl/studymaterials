import torch 
import numpy as np
import torch.nn as nn 

from utils import clones

class MultiHeadedAttention(nn.Module):
    
    def __init__(self, h, d_model, dropout=0.1):
        # Take in model size and number of heads

        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0

        self.d_k = d_model // h
        self.h = h   #number of heads
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        
        if mask is not None:
            mask = mask.unsqueeze(1)

        nbatches = query.size(0)



