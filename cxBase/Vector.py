'''
Created on Apr 29, 2014

@author: cx
'''

from copy import deepcopy
import math
class VectorC(object):
    def Init(self):
        self.hDim = {}
        
    def __init__(self,hDict = {}):
        self.Init()
        if {} != hDict:
            self.hDim = deepcopy(hDict)
        
        
    def __mul__(self,vb):
        if (type(vb) == float) | (type(vb) == int):
            res = VectorC(self.hDim)
            for item in res.hDim:
                res.hDim[item] *= vb
            return res
            
            
        else:
            score = 0
            for dim in self.hDim:
                if dim in vb.hDim:
                    score += self.hDim[dim] * vb.hDim[dim]
            return score
    
    def __div__(self,value):
        return self.__mul__(1.0/value)
    
    def Mod(self,level=2):
        score = 0
        for dim,value in self.hDim.items():
            score += math.pow(value,2)
        score = math.pow(value,0.5)
        return score
    
    @staticmethod
    def cosine(vA,vB):
        return (vA*vB)/(vA.Mod() * vB.Mod())
            
                
        
    