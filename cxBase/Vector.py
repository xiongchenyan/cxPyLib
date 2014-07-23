'''
Created on Apr 29, 2014

@author: cx
'''
'''
add KL divergence and two-way KL
'''

from copy import deepcopy
import math,json
class VectorC(object):
    def Init(self):
        self.hDim = {}
        self.Key = ""
        
    def __init__(self,InData = {}):
        self.Init()
        if {} != InData:
            if type(InData) == dict:
                self.hDim = deepcopy(InData)
            if type(InData) == list:
                self.hDim = dict(zip(InData,range(len(InData))))
    
    
    def dumps(self):
        return json.dumps(self.hDim)
    def loads(self,line):
        self.hDim = json.loads(line)
        
        
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
        res.Key = deepcopy(self.Key,memo)
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
    
    def GetDim(self,name):
        if name in self.hDim:
            return self.hDim
        return 0
       
    
    def Normalize(self):
        cnt = 0
        for item in self.hDim:
            cnt += self.hDim[item]
        if 0 == cnt:
            return
        for item in self.hDim:
            self.hDim[item] /= cnt
            
    
    
    @staticmethod
    def cosine(vA,vB):
#         InnerProd = vA*vB
#         print "inner prod [%f] mod [%f][%f]" %(InnerProd,vA.Mod(),vB.Mod())
        
        return (vA*vB)/(vA.Mod() * vB.Mod())
            
    @staticmethod
    def KL(vA,vB):
        vMidA = deepcopy(vA)
        vMidB = deepcopy(vB)
        vMidA.Normalize()
        vMidB.Normalize()        
        score = 0
        for dim,value in vMidA.hDim.items():
            if value == 0:
                continue
            score += math.log(value / vMidB.GetDim(dim)) * value

        return score
    
    @staticmethod
    def TwoWayKL(vA,vB):
        vSum = vA + vB
        score = 0.5 * VectorC.KL(vA,vSum)
        score += 0.5 * VectorC.KL(vB,vSum)
        return score
        
  
        
    