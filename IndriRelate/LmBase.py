'''
Created on my MAC Jun 10, 2015-4:34:12 PM
What I do:
separate LmBaseC to here

What's my input:

What's my output:

@author: chenyanxiong
'''

'''
Jun 10:
added KL,JS,distance (with protection)

'''

import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from IndriRelate.QueryPreprocess import *
from IndriSearch.IndriDocBase import IndriDocBaseC
import math
from IndriRelate.IndriPackedRes import *
from IndriRelate.CtfLoader import *
from cxBase.TextBase import TextBaseC
from cxBase.base import DiscardStopWord,ContainNonLetter
import copy
import pickle
from cxBase.Vector import VectorC
import logging
class LmBaseC(object):
    
    def __init__(self,data = ""):
        self.Init()        
        if "" == data:
            return
        if type(data) == list:
            data = '\t'.join(data)
        if type(data) in [str,unicode]:
            self.SetFromRawText(data)
            return
        if type(data) == PackedIndriResC:
            self.SetFromPackedDoc(data)
            return
        if type(data) == IndriDocBaseC:
            self.SetFromPackedDoc(data)
            return
        logging.WARN("Init LmBaseC type [%s] not recognized", str(type(data)))    
    
    def Init(self):
        self.hTermTF = {}
        self.len = 0
        return True
    
    def empty(self):
        if self.len == 0:
            return True
        return False
    def clear(self):
        self.hTermTF.clear()
    
    def __deepcopy__(self,memo):
        lm = LmBaseC()
        lm.hTermTF = copy.deepcopy(self.hTermTF, memo)
        lm.len = self.len
        return lm
    
    def SetFromPackedDoc(self,PackedDoc):
        for pos in PackedDoc.lPosition:
            term = PackedDoc.lTerm[pos]
#             if term != "[OOV]":
            self.Insert(term)
        return True
    
    
    def SetFromRawText(self,text):
        self.AddRawText(text)
    
    def Insert(self,term,tf = 1):
        if not term in self.hTermTF:
            self.hTermTF[term] = 0
        self.hTermTF[term] += tf
        self.len += tf
        
    def AddRawText(self,text):
        lTerm = TextBaseC.RawClean(text).split()
        for term in lTerm:
            self.Insert(term)
        
    def SetFromDict(self,hTerm):
        self.hTermTF = copy.deepcopy(hTerm)
        self.CalcLen()
        return
        
    
    def AddIdfFactor(self,CtfCenter):
        for term in self.hTermTF.keys():
            LogIdf = CtfCenter.GetLogIdf(term)
            self.hTermTF[term] *= LogIdf
        self.CalcLen()
        return True
        
        
    
    
    def load(self,InName):
        f = open(InName)
        self.hTermTF = pickle.load(f)
        self.CalcLen()
        f.close()
    def dump(self,OutName):
        f = open(OutName,'w')
        pickle.dump(self.hTermTF,f)
        f.close()
    
    def dumps(self):
        return json.dumps(self.hTermTF)
    def loads(self,line):
        self.hTermTF = json.loads(line)
        self.CalcLen()    
        
    def CalcLen(self):
        self.len = 0
        for item in self.hTermTF:
            self.len += self.hTermTF[item]
        return
    
    
    def GetLen(self):
        return self.len
    
    def GetTF(self,term):
        if not term in self.hTermTF:
            return 0
        return self.hTermTF[term]
    
    def GetTFProb(self,term):
        if 0 == self.len:
            return 0
        return self.GetTF(term) / float(self.len)


    
    @staticmethod
    def Cosine(LmA,LmB):
        return LmA * LmB
    
    def __add__(self,LmB):
        Lm = copy.deepcopy(self)
        for dim in LmB.hTermTF:
            if not dim in Lm.hTermTF:
                Lm.hTermTF[dim] = LmB.hTermTF[dim]
            else:
                Lm.hTermTF[dim] += LmB.hTermTF[dim]
        Lm.CalcLen()
        return Lm
    
    def __mul__(self,InData):
        prod = 0
        
        if (type(InData) == float) | (type(InData) == int):
            Lm = copy.deepcopy(self)
            for dim in Lm.hTermTF:
                Lm.hTermTF[dim] *= InData
            Lm.CalcLen()
            return Lm
        
        for term in self.hTermTF:
            prod += self.GetTFProb(term) * InData.GetTFProb(term)
        return prod
    
    def TransferToVectorWithIdf(self,CtfCenter):
        if self.len == 0:
            return self
        v = VectorC(self.hTermTF)
        v /= self.len
        for item in v.hDim:
            CTF = CtfCenter.GetCtfProb(item)
            v.hDim[item] *= math.log(1.0/CTF)
        return v
            
    
    @staticmethod
    def TfIdfCosine(LmA,LmB,CtfCenter):
        
        
        if (LmA.len == 0) | ( LmB.len == 0):
            return 0
        
        vA = LmA.TransferToVectorWithIdf(CtfCenter)
        vB = LmB.TransferToVectorWithIdf(CtfCenter)
        
        score =  VectorC.cosine(vA, vB)
        
        print "cosine [%f] of:\n%s\n%s" %(score, json.dumps(vA.hDim),json.dumps(vB.hDim))
        return score
    
    
    
    @staticmethod
    def Similarity(LmA,LmB,CtfCenter,SimMetric):
        
#         if (LmA.len == 0) | (LmB.len == 0):
#             return 0
        
        vA = LmA.TransferToVectorWithIdf(CtfCenter)
        vB = LmB.TransferToVectorWithIdf(CtfCenter)
        
        score =  VectorC.Similarity(vA, vB, SimMetric)
        
#         print "similarity [%s] [%f] of:\n%s\n%s" %(SimMetric,score, json.dumps(vA.hDim),json.dumps(vB.hDim))
        return score
    
  
    
    @staticmethod
    def MakeLmForDocs(lDoc):
        lLm = []
        for doc in lDoc:
            Lm = LmBaseC()
            Lm.SetFromPackedDoc(doc)
            lLm.append(copy.deepcopy(Lm))
        return lLm        