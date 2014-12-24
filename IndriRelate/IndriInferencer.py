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
from IndriRelate.IndriDocBase import IndriDocBaseC
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from IndriRelate.QueryPreprocess import *
import math
from IndriRelate.IndriPackedRes import *
from IndriRelate.CtfLoader import *
from cxBase.TextBase import TextBaseC
from cxBase.base import DiscardStopWord,ContainNonLetter
import copy
import pickle
from cxBase.Vector import VectorC
class LmBaseC(object):
    
    def __init__(self,data = ""):
        self.Init()        
        if "" == data:
            return
        if type(data) in [str,unicode]:
            self.SetFromRawText(data)
            return
        if type(data) == PackedIndriResC:
            self.SetFromPackedDoc(data)
            return
        if type(data) == IndriDocBaseC:
            self.SetFromPackedDoc(data)
        print "type [%s] not recognized" %(str(type(data)))    
    
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

    @staticmethod
    def TfIdfCosine(LmA,LmB,CtfCenter):
        vA = VectorC(LmA.hTermTF)
        vB = VectorC(LmB.hTermTF)
        
        if (LmA.len == 0) | ( LmB.len == 0):
            return 0
        
        vA /= LmA.len
        vB /= LmB.len
        
        
        for item in vA.hDim:
            CTF = CtfCenter.GetCtfProb(item)
            vA.hDim[item] *= math.log(1.0/CTF)
        for item in vB.hDim:
            CTF = CtfCenter.GetCtfProb(item)
            vB.hDim[item] *= math.log(1.0/CTF)
        
        
        score =  VectorC.cosine(vA, vB)
        
        print "cosine [%f] of:\n%s\n%s" %(score, json.dumps(vA.hDim),json.dumps(vB.hDim))
        return score
        
        
        
        

    
def MakeLmForDocs(lDoc):
    lLm = []
    for doc in lDoc:
        Lm = LmBaseC()
        Lm.SetFromPackedDoc(doc)
        lLm.append(copy.deepcopy(Lm))
    return lLm    

#inferencer for language modeling
class LmInferencerC(object): 
    
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
        res = self.LmFunc(tf, CorpusP, DocLen)
        return res
    def LmFunc(self,tf,CorpusP,DocLen):
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
    
    def BM25Term(self,term,Lm,CtfCenter):
        N = CtfCenter.TotalCnt;
        df = CtfCenter.GetCtf(term)
        tf = Lm.GetTF(term)
        DocLen = Lm.GetLen()
        b = 0.75
        k1 = 1.2        
        AvgDocLen = 800   #works for both CW09 and CW12
        
        score = math.log((N-df + 0.5)/(df+0.5)) * (tf)/(tf+k1*(1-b + b*DocLen/AvgDocLen))       
        return score
    
    def Bm25(self,query,Lm,CtfCenter):
        score = 0
        lTerm = query.split()
        for term in lTerm:
            score += self.BM25Term(term, Lm, CtfCenter)
        return score
    
    def CoorMatch(self,query,Lm):
        lQTerm = query.split()
        if len(lQTerm) == 0:
            return 0
        cnt = 0
        for term in lQTerm:
            if term in Lm.hTermTF:
                cnt += 1
        return cnt
        
    
    def TFIDF(self,query,Lm,CtfCenter):
        lScore = []
        lTerm = query.split()
        for term in lTerm:
            score = Lm.GetTFProb(term) * math.log(CtfCenter.GetCtfProb(term))
            lScore.append(score)
        MeanScore = 0
        if len(lScore) != 0:
            MeanScore = sum(lScore) / float(len(lScore))
        return MeanScore
    
    def SDMQueryInfer(self,query,DocText,CtfCenter):
        Lm = LmBaseC(DocText)
        
        UnigramScore = self.InferQuery(query,Lm,CtfCenter)
        
        NearScore = 0
        UWScore = 0
        lQTerm = query.split()
        lDocTerm = DocText.split()
        
        NearSize = 1
        UWSize = 8
        
        for i in range(len(lQTerm) - 1):
            lBigram = lQTerm[i:i+2]
            NearScore += self.Near(lBigram, NearSize, lDocTerm, CtfCenter)
            UWScore += self.UW(lBigram, UWSize, lDocTerm, CtfCenter)
        
        res = 0.8 * UnigramScore + 0.1 * NearScore + 0.1 * UWScore
        return res
    
        
    def Near(self,lQTerm,NearSize,lDocTerm,CtfCenter):
        tf = self.NearCnt(lQTerm, NearSize, lDocTerm)
        CtfP = 1
        for term in lQTerm:
            CtfP *= CtfCenter.GetCtfProb(term)
        if (0 == CtfP):
            CtfP = 0.5
        
        res = self.LmFunc(tf,CtfP,len(lDocTerm))
        return res    
        
    def NearCnt(self,lQTerm,NearSize,lDocTerm):
        '''
        go through lDocTerm,
        if meet a qterm, always update the lQP to this position
        if meet last qterm:
            check if lQP satisfy NearSize requirements
            if so:
                res += 1
                reset lQP to -1
        '''
        res = 0
        lQP = [-1] * len(lQTerm)
        hQ = dict(zip(lQTerm,range(len(lQTerm))))
        
        for i in range(len(lDocTerm)):
            if not lDocTerm[i] in hQ:
                continue
            Qloc = hQ[lDocTerm[i]]
            lQP[Qloc] = i
            if Qloc == len(lQP):
                #is last term, now check if is a match
                if self.IsANearMatch(lQP, NearSize):
                    res += 1
                    lQP = [-1] * len(lQTerm)
        return res
        
        
        
        
    def IsANearMatch(self,lQP,NearSize):
        for i in range(len(lQP) - 1):
            if lQP[i] == -1:
                return False
            if lQP[i + 1] - lQP[i] <= 0:
                return False
            if lQP[i + 1] - lQP[i] > NearSize:
                return False
        return True
        
        
    def UW(self,lQTerm,UWSize,lDocTerm,CtfCenter):
        tf = self.UWCnt(lQTerm, UWSize, lDocTerm)
        CtfP = 1
        for term in lQTerm:
            CtfP *= CtfCenter.GetCtfProb(term)
        if (0 == CtfP):
            CtfP = 0.5
        
        res = self.LmFunc(tf,CtfP,len(lDocTerm))
        return res
        
    def UWCnt(self,lQTerm,UWSize,lDocTerm):
        '''
        go through lDocTerm,
        if meet a qterm, always update the lQP to this position
        if meet last qterm:
            check if lQP satisfy UW requirements
            if so:
                res += 1
                reset lQP to -1
        '''
        res = 0
        lQP = [-1] * len(lQTerm)
        hQ = dict(zip(lQTerm,range(len(lQTerm))))
        
        for i in range(len(lDocTerm)):
            if not lDocTerm[i] in hQ:
                continue
            Qloc = hQ[lDocTerm[i]]
            lQP[Qloc] = i
            if Qloc == len(lQP):
                #is last term, now check if is a match
                if self.IsAUWMatch(lQP, UWSize):
                    res += 1
                    lQP = [-1] * len(lQTerm)
        return res    
    
    def IsAUWMatch(self,lQP,UWSize):
        MinP = min(lQP)
        MaxP = max(lQP)
        if MinP == -1:
            return False
        if (MaxP - MinP) > UWSize:
            return False
        return True
        
        
        
    
    
 
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


