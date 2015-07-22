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
                self.hDim = dict(zip(range(len(InData)),InData))
    
    
    def dumps(self):
        return json.dumps(self.hDim)
    def loads(self,line):
        self.hDim = json.loads(line)
    
    def IsEmpty(self):
        return self.hDim == {}    
        
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
    
    def __sub__(self,vB):
        res = deepcopy(self)
        for item in vB.hDim:
            if not item in res.hDim:
                res.hDim[item] = vB.hDim[item] * (-1)
            else:
                res.hDim[item] -= vB.hDim[item]
        return res
    
    def __abs__(self):
        res = deepcopy(self)
        for item in self.hDim:
            res.hDim[item] = math.fabs(self.hDim[item])
        return res
    
    
    
            
    
    
    def Mod(self,level=2):
        score = 0
        for dim,value in self.hDim.items():
            score += math.pow(value,2)
        score = math.pow(score,0.5)
        return score
    
    def GetDim(self,name):
        if name in self.hDim:
            return self.hDim[name]
        return 0
       
    
    def Normalize(self):
        cnt = 0
        for item in self.hDim:
            cnt += self.hDim[item]
        if 0 == cnt:
            return
        for item in self.hDim:
            self.hDim[item] /= float(cnt)
            
    @staticmethod
    def Similarity(vA,vB,SimMetric):
        if SimMetric == 'cosine':
            return VectorC.cosine(vA, vB)
        if SimMetric == 'l2':
            return -VectorC.L2Distance(vA, vB)
        if SimMetric == 'js':
            return -VectorC.TwoWayKL(vA, vB)
        if SimMetric == 'kl':
            return -VectorC.KL(vA, vB)
        return 0
    
    @staticmethod
    def cosine(vA,vB):
#         InnerProd = vA*vB
#         print "inner prod [%f] mod [%f][%f]" %(InnerProd,vA.Mod(),vB.Mod())
        Ma = vA.Mod()
        Mb = vB.Mod()
        if (0 == Ma) | (0 == Mb):
            return 0
        return (vA*vB)/(vA.Mod() * vB.Mod())
    @staticmethod
    def L2Distance(vA,vB):
        res = 0
        hAll = dict(vA.hDim)
        hAll.update(vB.hDim)
        lAllKey = hAll.keys()
        for key in lAllKey:
            a = vA.GetDim(key)
            b = vB.GetDim(key)
            res += (a-b)**2
        res = math.sqrt(res)
        return res
    
    @staticmethod
    def PointWiseL2(vA,vB):
        res = VectorC()
        hAll = dict(vA.hDim)
        hAll.update(vB.hDim)
        lAllKey = hAll.keys()
        for key in lAllKey:
            a = vA.GetDim(key)
            b = vB.GetDim(key)
            res.hDim[key] = (a-b)**2
        return res     
        
            
    @staticmethod
    def KL(vA,vB):
        vMidA = deepcopy(vA)
        vMidB = deepcopy(vB)
        vMidA.Normalize()
        vMidB.Normalize()  
        MaxKL = 20
        if vMidA.IsEmpty() | vMidB.IsEmpty():
            return MaxKL      
        score = 0
        for dim,value in vMidA.hDim.items():
            if value == 0:
                continue
            if 0 == vMidB.GetDim(dim):
                continue
            score += math.log(value / vMidB.GetDim(dim)) * value

        return score
    
    @staticmethod
    def TwoWayKL(vA,vB):
        vSum = vA + vB
        score = 0.5 * VectorC.KL(vA,vSum)
        score += 0.5 * VectorC.KL(vB,vSum)
        return score
        
  
    
    