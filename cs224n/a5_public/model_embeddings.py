#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CS224N 2019-20: Homework 5
model_embeddings.py: Embeddings for the NMT model
Pencheng Yin <pcyin@cs.cmu.edu>
Sahil Chopra <schopra8@stanford.edu>
Anand Dhoot <anandd@stanford.edu>
Michael Hahn <mhahn2@stanford.edu>
"""

import torch.nn as nn

# Do not change these imports; your module names should be
#   `CNN` in the file `cnn.py`
#   `Highway` in the file `highway.py`
# Uncomment the following two imports once you're ready to run part 1(j)

from cnn import CNN
from highway import Highway


# End "do not change"

class ModelEmbeddings(nn.Module):
    """
    Class that converts input words to their CNN-based embeddings.
    """

    def __init__(self, word_embed_size, vocab):
        """
        Init the Embedding layer for one language
        @param word_embed_size (int): Embedding size (dimensionality) for the output word
        @param vocab (VocabEntry): VocabEntry object. See vocab.py for documentation.

        Hints: - You may find len(self.vocab.char2id) useful when create the embedding
        """
        super(ModelEmbeddings, self).__init__()
        
        ### YOUR CODE HERE for part 1h
        self.word_embed_size = word_embed_size
        self.vocab = vocab
        self.embed = nn.Embedding(len(self.vocab.char2id), 50)
        self.cnn = CNN(50, self.word_embed_size, 5, 1)
        self.highway = Highway(self.word_embed_size)
        
        ### END YOUR CODE

    def forward(self, input):
        """
        Looks up character-based CNN embeddings for the words in a batch of sentences.
        @param input: Tensor of integers of shape (sentence_length, batch_size, max_word_length) where
            each integer is an index into the character vocabulary

        @param output: Tensor of shape (sentence_length, batch_size, word_embed_size), containing the
            CNN-based embeddings for each word of the sentences in the batch
        """
        ### YOUR CODE HERE for part 1h
        #number of words is sentence_length * batch_size 
        #(10, 5, 21) = (l, b, mword)
        l, b, mword = input.shape
        x = input.view(l*b, mword)
        #print('l*b, mword', x.shape)
        x = self.embed(x) #(l*b, mword, echar)
        #print('l*b, mword, echar', x.shape)
        x = x.permute(0, 2, 1) #(l*b, echar, mword)
        #print('l*b, echar, mword', x.shape)
        x = self.cnn(x) #(l*b, eword)
        #print('l*b, eword', x.shape)
        x = self.highway(x) #(l*b, eword)
        #print('l*b, eword', x.shape)
        x = x.view(l, b, -1)
        #print('l, b, eword', x.shape)
        return x
        ### END YOUR CODE

