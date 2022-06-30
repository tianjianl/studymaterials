import torch
import torch.nn as nn

def clones(module, N):

    #Creates N clones of module

    return nn.Modulelist([copy.deepcopy(module) for _ in range(N)])
