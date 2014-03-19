'''
Created on Dec 5, 2013
implement the simple language model and (not now) bm25 relevance model in indri
classes:
    LmBaseC (calc tf, keep tf, etc)
    Inferencer(bm25 and lm)
12/9/2013
    Lm inferencer done,
    unit test finished, With Dir smoothing, result same with Indri's output    
@author: cx
'''
import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
from IndriRelate.QueryPreprocess import *
import math
from IndriRelate.IndriPackedRes import *
from IndriRelate.CtfLoader import *
from cxBase.base import DiscardStopWord,ContainNonLetter
import copy
import pickle


class LmBaseC:
    
    def __init__(self):
        self.Init()        
    
    def Init(self):
        self.hTermTF = {}
        self.len = 0
        return True
    
    def SetFromPackedDoc(self,PackedDoc):
        for pos in PackedDoc.lPosition:
            term = PackedDoc.lTerm[pos]
#             if term != "[OOV]":
            self.Insert(term)
        return True
    
    def Insert(self,term,tf = 1):
        if not term in self.hTermTF:
            self.hTermTF[term] = 0
        self.hTermTF[term] += tf
        self.len += tf
    def AddRawText(self,text):
        lTerm = text.split(' ')
        for term in lTerm:
            self.Insert(term)
        
    def SetFromDict(self,hTerm):
        self.hTermTF = copy.deepcopy(hTerm)
        self.CalcLen()
        return
        
    
    
    def load(self,InName):
        f = open(InName,'r')
        self.hTermTF = pickle.load(f)
        self.CalcLen()
        f.close()
    def dump(self,OutName):
        f = open(OutName,'w')
        pickle.dump(self.hTermTF,f)
        f.close()
        
        
    def CalcLen(self):
        self.len = 0
        for item in self.hTermTF:
            self.len += self.hTermTf[item]
        return
    
    
    def GetTF(self,term):
        if not term in self.hTermTF:
            return 0
        return self.hTermTF[term]
    
    def GetTFProb(self,term):
        return self.GetTF(term) / float(self.len)
    def __deepcopy__(self,memo):
        Lm = LmBaseC()
        Lm.len = self.len
        Lm.hTermTF = copy.deepcopy(self.hTermTF)
        return Lm
    
def MakeLmForDocs(lDoc):
    lLm = []
    for doc in lDoc:
        Lm = LmBaseC()
        Lm.SetFromPackedDoc(doc)
        lLm.append(copy.deepcopy(Lm))
    return lLm    

#inferencer for language modeling
class LmInferencerC: 
    
    def Init(self):
#         self.DirSudoCnt = 2500
        self.DirPrior = 0.01
#         self.JmStrength = 0.4
        self.JmPrior = 0.001    
        self.SmoothType = "dir"
        self.SetSmoothType('dir')
        return True
    
    def __init__(self,SmoothType = 'dir'):
        self.Init()    
        self.SetSmoothType(SmoothType)    

    
    #will modify parameters based on targe smooth type:
        #Dir: JmStrength = 0
        #Jm: DirSudoCnt = 0
    def SetSmoothType(self,TargetSmooth):
        self.SmoothType = TargetSmooth
        self.JmStrength = 0.4
        self.DirSudoCnt = 2500
        if "twostage" == TargetSmooth:
            return True
        if "dir" == TargetSmooth:
            self.JmStrength = 0
            return True
        if "jm" == TargetSmooth:
            self.DirSudoCnt = 0
            return True
        print "smooth type [%s] not defined" %(TargetSmooth)
        return False
    
    #term: term to inference
    #Lm: LmBaseC, the doc tfs
    #CtfCenter: to get corpus prob: TermCtfC 
    def InferTerm(self,term,Lm,CtfCenter):
        tf = Lm.GetTF(term)
        DocLen = Lm.len
        CorpusP = CtfCenter.GetCtfProb(term)
        
        #set constrant CTF for OOV words
        if (0 == tf) & (0 == CorpusP):
            CorpusP = 0.5 #indri default
#         print "term [%s] tf [%f] Ctf [%f]"%(term,float(tf)/DocLen,CorpusP)
        res = (tf +self.DirSudoCnt * CorpusP) / (DocLen + self.DirSudoCnt) * (1 - self.JmStrength)
        res += self.JmStrength * CorpusP
        return res


    def InferQuery(self,query,Lm,CtfCenter):
        #dealing with words not exist (or stopword), just ignore it in query, (the term is discarded)
        #discard stopword
#         print "preclean [%s]" %(query)
        query = CleanQuery(query)
#         print "after [%s]"%(query)                           
        lTerm = query.split()
        Prob = 0
        if len(lTerm) == 0:
            return math.log(math.exp(-10))
        for term in lTerm:
            p = self.InferTerm(term,Lm,CtfCenter)   
            if 0 == p:
                continue         
#             print "[%s][%s] prob [%f][%f]" %(query,term,p,math.log(p))
            Prob += math.log(p)            
#         print "infer prob [%f]" %(Prob)        
        Prob /= len(lTerm)
        return Prob
    
 
def CleanQuery(query):
    lTerm = query.split(" ")
    lRes = []
    for term in lTerm:
#         if ContainNonLetter(term):
#             continue
        lRes.append(term)
    query = DiscardStopWord(" ".join(lRes))
    return query
     
    
def InferProbForDocs(query,lDoc,CtfCenter):
    lProb = []
    LmModel = LmInferencerC()
    for doc in lDoc:
        Lm = LmBaseC()
        Lm.SetFromPackedDoc(doc)
        lProb.append(LmModel.InferQuery(query,Lm,CtfCenter))
    return lProb

def UnitTest(query, DocInName,CtfInName,OutName):
    lDoc = ReadPackedIndriRes(DocInName)
    CtfCenter = TermCtfC(CtfInName)
    out = open(OutName,"a")
    query = DiscardNonEnChar(query)
    lProb = InferProbForDocs(query,lDoc,CtfCenter)
    for i in range(len(lProb)):
        print >> out, "%s\t%s\t%f" %(query,lDoc[i].DocNo,lProb[i])
    out.close()


