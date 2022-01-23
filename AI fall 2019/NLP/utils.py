import os
import sys
import numpy as np

class Tree(object):
    
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def addChild(self, child):
        self.children.append(child)



def extractSymbol(s, k):
    while s[k] == ' ':
        k += 1            #skipping white spaces

    if s[k] == '(' or s[k] == ',' or s[k] == ')':
        return s[k], k+1
    
    if s[k].isalpha == False:
        raise ValueError('invaid character at input '+str(k))

    m = ""
    while s[k].isalpha():
        m = m + s[k]
        k += 1
    
    return m, k

def extractExpression(s, k):
    m, q = extractSymbol(s, k)
    if m.isalpha() == False:
        raise ValueError('invalid character at index '+str(k))

    T = Tree(m, [])
    n, peek = extractSymbol(s, q)
    if n != '(':
        return T, q

    q = peek
    while True:
        c, q = extractExpression(s, q)
        T.addChild(c)
        n, q = extractSymbol(s, q)
        if n == ')':
            return T, q

        if n != ',':
            raise ValueError('invalid character at index '+str(q))


def printTree(T):
    print(T.root)
    if len(T.children) != 0:
        print(T.root+'s children are')
    for children in T.children:
        printTree(children)


#teststring = 'S(NP(Pron(I)),VP(Verb(fish)))'
#testtree, length = extractExpression(teststring, 0)
#printTree(testtree)
        
