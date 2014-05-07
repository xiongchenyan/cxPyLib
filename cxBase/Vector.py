'''
Created on Apr 29, 2014

@author: cx
'''

from copy import deepcopy
import math
class VectorC(object):
    def Init(self):
        self.hDim = {}
        
    def __init__(self,InData = {}):
        self.Init()
        if {} != InData:
            if type(InData) == dict:
                self.hDim = deepcopy(InData)
            if type(InData) == list:
                self.hDim = dict(zip(InData,range(len(InData))))
    
    
        
        
    def __mul__(self,vb):
        if (type(vb) == float) | (type(vb) == int):
            res = deepcopy(self)
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
    
    
    def __deepcopy__(self,memo):
        res = VectorC()
        res.hDim = deepcopy(self.hDim,memo)
        return res
    
    def __add__(self,vB):
        res = deepcopy(self)
        for item in vB.hDim:
            if not item in res.hDim:
                res.hDim[item] = vB.hDim[item]
            else:
                res.hDim[item] += vB.hDim[item]
        return res
    
    
    def Mod(self,level=2):
        score = 0
        for dim,value in self.hDim.items():
            score += math.pow(value,2)
        score = math.pow(score,0.5)
        return score
    
    
    
    
    @staticmethod
    def cosine(vA,vB):
        InnerProd = vA*vB
#         print "inner prod [%f] mod [%f][%f]" %(InnerProd,vA.Mod(),vB.Mod())
        
        return (vA*vB)/(vA.Mod() * vB.Mod())
            
                
        
    