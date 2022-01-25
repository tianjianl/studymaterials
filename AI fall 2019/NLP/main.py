import sys
from utils import Tree, extractSymbol, extractExpression, printTree

def parse(treenode, now, ans): 
    if treenode.root == 'NP':
        now += 1
        if len(treenode.children) != 1:
            for temp in treenode.children:
                if temp.root != 'Det':
                    ans[temp.children[0].root] = now
    
    elif treenode.root == 'VP':
        for temp in treenode.children:
            if temp.root == 'NP' or 'PP':
                now, ans = parse(temp, now, ans)

    elif treenode.root == 'PP':
        for temp in treenode.children:
            if temp.root == 'NP':
                now, ans = parse(temp, now, ans)

    return now, ans

def main(sentence, ans):
    t, _ = extractExpression(sentence, 0)
    
    #getting all NPs
    now = 0
    for child in t.children:
        now, ans = parse(child, now, ans)    

    return ans
        
def setPrint(s):
    
    for item in s:
        if type(s[item]) == tuple:
            print(item+'(X'+str(s[item][0])+',X'+str(s[item][1])+')')
        else:
            print(item+'(X'+str(s[item])+').')


if __name__ == '__main__':
    answer_set = {}
    #default_sentence = 'S(NP(Name(Amy)),VP(Verb(gave),NP(Det(the),Adj(pretty),Noun(flowers)),PP(Prep(to),NP(Det(the),Adj(small),Noun(boy)))))'
    default_sentence = 'S(NP(Det(The),Adj(small),Noun(boy)),VP(Verb(bought),NP(Det(the),Adj(old),Noun(book)),PP(Prep(from),NP(Det(the),Adj(old),Noun(man)))))'  
    
    answer_set = main(default_sentence, answer_set)
    
    setPrint(answer_set) 
