import argparse
import numpy as np
import sys
import random

def chooseFromDist(p):
    #Given probability distribution p, return values from 1, 2 according to their probability
    #input p should be a list of probabities
    #p.sum should be 1
    
    k = len(p) - 1 
    u = [0 for _ in range(k+1)]

    u[0] = p[0]
    for i in range(1, k+1):
        u[i] = u[i-1] + p[i]
    
    x = random.random()
    for i in range(0, k):
        if x < u[i]:
            return i
    return k

def check_chooseFromDist(p=[0.2,0.3,0.5]):
    print("hello world")
    count = [0 for _ in range(len(p))]
    for i in range(10000):
        count[chooseFromDist(p)] += 1
        
    print(count)
    print("the approximate number of the printed list should be [2000, 3000, 5000]")

def rollDice(NDice, NSides):
    #roll a Dice with 'NSides' sides 'NDice' times
    #returns a list of the rolled outputs
    output = []
    prob = [(1.0)/NSides for _ in range(NSides)]
    for _ in range(NDice):
        output.append(chooseFromDist(prob)+1)

    return output

def check_rollDice(NDice=15, NSides=3):
    print(rollDice(NDice, NSides))

def chooseDice(Score, LoseCount, WinCount, NDice, M):
    #Score: list of current state [x, y]
    #returns the dice to roll
    X, Y = Score[0], Score[1]
    K = NDice
    f = [0 for _ in range(K+1)]
    for j in range(1, K+1):
        if WinCount[X,Y,j] + LoseCount[X,Y,j] == 0:
            f[j] = 0.5
        else:
            f[j] = WinCount[X,Y,j]/(WinCount[X,Y,j]+LoseCount[X,Y,j])
    
    B = np.argmax(f)
    g = np.sum(f) - f[B]
    T = 0
    for j in range(0, K+1):
        T += WinCount[X, Y, j] + LoseCount[X, Y, j]

    p = []
    temp = (T*f[B] + M)/(T*f[B] + K*M)
    for j in range(1, K+1):
        if j == B:
            p.append(temp)
        else:
            p.append((1-temp)*(T*f[j]+M)/(g*T+(K-1)*M))

    return p
    #return choosefromDist(p)+1
def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    Score = [0, 0]
    states = []
    while True:
        
        dice_prob = chooseDice(Score, LoseCount, WinCount, NDice, M)
        num_to_roll = chooseFromDist(dice_prob)+1
        outcomes = rollDice(num_to_roll, NSides)
        states.append((Score[0], Score[1], num_to_roll))
        Score[0] += np.sum(outcomes)
        if Score[0] >= LTarget:
            if Score[0] <= UTarget: #won
                flag = True
            else: #lost
                flag = False
            break
        Score[0], Score[1] = Score[1], Score[0]
    for state in reversed(states):
        if flag == True:
            WinCount[state[0], state[1], state[2]] += 1
            flag = False
        else:
            LoseCount[state[0], state[1], state[2]] += 1
            flag = True

    return WinCount, LoseCount


def extractAnswer(WinCount, LoseCount):
    #shape of WinCount should be (LTarget, LTarget, NDice+1)
    #returns two LTarget*LTarget Arrays
    #first one is the correct move, second is the probability of winning
    LTarget = WinCount.shape[0]
    best_move = [[0 for _ in range(LTarget+1)] for _ in range(LTarget+1)]

    win_prob = [[0 for _ in range(LTarget+1)] for _ in range(LTarget+1)]

    NDice = WinCount.shape[2] - 1
    for i in range(LTarget):
        for j in range(LTarget):
            f = []
            for k in range(1, NDice+1):
                if WinCount[i,j,k] + LoseCount[i,j,k] == 0:
                    f.append(0.0)
                else:
                    f.append(WinCount[i,j,k]/(WinCount[i,j,k]+LoseCount[i,j,k]))
            #f = [WinCount[i,j,k]/(WinCount[i,j,k]+LoseCount[i,j,k]) for k in range(1, NDice+1)]
            best_move[i][j] = np.argmax(f)+1
            win_prob[i][j] = np.max(f)
            
    return best_move, win_prob

def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    LoseCount = np.zeros((LTarget, LTarget, NDice+1))
    WinCount = np.zeros((LTarget, LTarget, NDice+1))
    
    for _ in range(NGames):
        WinCount, LoseCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

    mat1, mat2 = extractAnswer(WinCount, LoseCount)
    for i in range(LTarget):
        print(mat1[i][:-1])
    
    for i in range(LTarget):
        print(mat2[i][:-1])
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--NDice", type=int, default=2)
    parser.add_argument("--NSides", type=int, default=2)
    parser.add_argument("--LTarget", type=int, default=4)
    parser.add_argument("--UTarget", type=int, default=4)
    parser.add_argument("--NGames", type=int, default=100000)
    parser.add_argument("--M", type=int, default=100)
    args = parser.parse_args()
    #check_chooseFromDist()
    #check_rollDice()
    prog3(args.NDice, args.NSides, args.LTarget, args.UTarget, args.NGames, args.M)

