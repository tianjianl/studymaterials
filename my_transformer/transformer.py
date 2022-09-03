import torch
import torch.nn as nn
from utils import clones
class EncoderDecoder(nn.Module):
    """
    A standard Encoder-Decoder architecture.
    """

    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super(EncoderDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.generator = generator

    def forward(self, src, tgt, src_mask, tgt_mask):
        return self.decode(self.encode(src, src_mask), src_mask, tgt, tgt_mask)


    def encode(self, src, src_mask):
        return self.encoder(self.src_embed(src), src_mask)


    def decode(self, memory, src_mask, tgt, tgt_mask):
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)


class Generator(nn.Module):
    """
    Linear + Softmax
    """
    def __init__(self, d_model, vocab):
        super(Generator, self).__init__()
        self.proj = nn.Linear(d_model, vocab # vocab = size of vocabulary 


    def forward(self, x):
        return log_softmax(self.proj(x), dim=-1)

class Encoder(nn.Module):
    """
    Encoder stack of N layers
    """
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = clones(layers, N)
        self.norm = LayerNorm(layer.size)
    
    def forward(self, x, mask):
        
        for layer in self.layers:
            x = layer(x, mask)

        return self.norm(x)
        
class LayerNorm(nn.Module):
    
    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps
    
    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2



class SubLayerConnection(nn.Module):
    """
    Residual Connection
    """

    def __init__(self, size, dropout):
        super(SubLayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        
        return x + self.dropout(sublayer(self.norm(x)))



