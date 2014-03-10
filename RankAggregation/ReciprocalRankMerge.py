'''
Created on Nov 20, 2013
merge multiple ranked list using reciprocal rank
@author: cx
'''
from operator import itemgetter

def ReciprocalRankMerge(lhRank):
    hMergeRes = {}    
    for i in range(len(lhRank)):
        for item in lhRank[i]:
            if (lhRank[i][item] == -1):
                continue
            score = 1.0 / lhRank[i][item]
            for j in range(i+1,len(lhRank)):
                if item in lhRank[j]:
                    score += 1.0 / lhRank[j][item]
                    lhRank[j][item] = -1
            lhRank[i][item] = -1
            hMergeRes[item] = score
    return hMergeRes

def TransToRankList(hMergeRank):
    lRank = []
    for item in hMergeRank:
        lRank.append((item,hMergeRank[item]))
    lRank.sort(key=itemgetter(1),reverse=True)
    return lRank
        
            
