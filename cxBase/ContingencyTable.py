'''
Created on Mar 27, 2014
calculate contingency table
input: two list of labels (predicted and ground truth for example)
output: a 2 dimension contingency, dim 1: predicted, dim 2: ground truth
@author: cx
'''


from base import *
def ContingencyTable(lPre,lTrue):
    lLabel = list(lPre)
    lLabel.extend(lTrue)
    lLabel = list(set(lPre + lTrue))
    lLabel.sort()
    hLabel = dict(zip(lLabel,range(len(lLabel))))
    
    lTable = CreatTwoDimList(len(hLabel),len(hLabel),0)
    
    for i in len(lPre):
        x = hLabel[lPre[i]]
        y = hLabel[lTrue[i]]
        lTable[x][y] += 1
    return lTable
    
    
    
    
    
    
    