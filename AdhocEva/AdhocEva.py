'''
Created on Feb 10, 2014
evaluate a rank, by given AdHocQRelC
2/10/2014: MAP supportted
@author: cx
'''
from AdhocQRel import *
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from AdhocMeasure import *
from cxBase.base import *
from cxBase.Conf import cxConfC
from operator import itemgetter
import math,json
class AdhocEvaC(object):
    
    def Init(self):
        self.AdhocQRel = AdhocQRelC()
        self.Depth = 20
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return

    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        lQRelIn = conf.GetConf("qrel")
        if type(lQRelIn) != list:
            lQRelIn = [lQRelIn]
        for QRelIn in lQRelIn:
            self.AdhocQRel.Load(QRelIn)
        self.Depth = conf.GetConf("evadepth",self.Depth)
        return True
    
    @staticmethod
    def ShowConf():
        print"qrel\nevadepth 20"
    
    
    
    
    def MAP(self,Qid,lDocNo):
        #evaluate the map
        #lDoc is ranked DocNo
        PosCnt = 0
        SumPrecision = 0
        #allow the maximum depth 1000
        Depth = 1000
        for i in range(min(len(lDocNo),Depth)):
            value = self.AdhocQRel.GetScore(Qid, lDocNo[i])
            if value != 0:
                PosCnt += 1
                SumPrecision += float(PosCnt) / float(i + 1)
        if 0 == PosCnt:
            return 0
        return SumPrecision / float(PosCnt)
    
    
    def Precision(self,qid,lDocNo):
        PosCnt = 0.0
        for i in range(min(len(lDocNo),self.Depth)):
            value = self.AdhocQRel.GetScore(qid, lDocNo[i])
            if value > 0:
                PosCnt += 1.0
        return PosCnt / self.Depth
            
    
    def BestDCG(self,qid):
        #calc the best possible NDCG from qrel
        lRelDoc = self.AdhocQRel.GetAllRelDoc(qid)
        if [] == lRelDoc:
#             print "no rel doc for [%s] best dcg 0" %(qid)
            return 0
        lRelDoc.sort(key=itemgetter(1),reverse=True)
        res = 0
        for i in range(min(len(lRelDoc),self.Depth)):
            res += (math.pow(2.0,lRelDoc[i][1]) - 1) / math.log(1 + i + 1)
#         print "[%s] best dcg: [%f]" %(qid,res)
        return res
    
    def DCG(self,qid,lDocNo):
        #calc DCG
        res = 0
        for i in range(min(len(lDocNo),self.Depth)):
            value = self.AdhocQRel.GetScore(qid, lDocNo[i])
            if value == 0:
                continue
            res += (math.pow(2.0,value) - 1) / math.log(1 + i + 1)
#         print "[%s] DCG [%f]" %(qid, res)
        return res
    
    def NDCG(self,qid,lDocNo):
        Z = self.BestDCG(qid)
        if 0 == Z:
            return 0
        return self.DCG(qid, lDocNo) / Z
    
    
    
    def PofRel(self,g):
        return (math.pow(2.0,g) - 1)/math.pow(2.0,self.AdhocQRel.MaxScore)
    
    def ERR(self,qid,lDocNo):      
        err = 0
        p = 1
        for i in range(min(len(lDocNo),self.Depth)):
            r = i + 1
            g = self.AdhocQRel.GetScore(qid, lDocNo[i]) 
            R = self.PofRel(g)
            err += p * R / r
            p = p * (1 - R)
        return err
    
    
    
    def EvaluatePerQ(self,Qid,lDocNo):
        print "start eva query [%s], doc num [%d]" %(Qid,len(lDocNo)) 
#         print json.dumps(lDocNo)
#         lMeasure.append(["map",self.MAP(Qid, lDocNo)])
#         lMeasure.append(['ndcg',self.NDCG(Qid,lDocNo)])
#         lMeasure.append(['err',self.ERR(Qid,lDocNo)])
        EvaRes = AdhocMeasureC()
        EvaRes.map = self.MAP(Qid, lDocNo)
        EvaRes.ndcg = self.NDCG(Qid,lDocNo)
        EvaRes.err = self.ERR(Qid,lDocNo)
        print "evares:\n%s" %(EvaRes.dumps(True))
        return EvaRes
    
    def EvaluateMul(self,lQid,llDocNo):
        EvaRes = AdhocMeasureC()
        for i in range(len(lQid)):
            mid = self.EvaluatePerQ(lQid[i],llDocNo[i])
            EvaRes = EvaRes + mid
        EvaRes = EvaRes / float(len(lQid))
        return EvaRes

    def SegDocNoFromDocs(self,lDoc):
        lDocNo = []
        for doc in lDoc:
            lDocNo.append(doc.DocNo)
        return lDocNo
    
    
    def EvaluateTrecOutFile(self,InName,OutName = ""):
        
        lEvaRes = []
        lQid,llDocNo = AdhocEvaC().ReadTrecOut(InName)
        
        for i in range(len(lQid)):
            lEvaRes.append(self.EvaluatePerQ(lQid[i], llDocNo[i]))
        
        Mean = AdhocMeasureMean(lEvaRes)
        
        if OutName != "":
            out = open(OutName,'w')
            for i in range(len(lQid)):
                print >>out,"%s\t%s" %(lQid[i],lEvaRes[i].dumps())
            print out,"mean\t%s" %(Mean.dumps())                    
        return lEvaRes
    
    
    @staticmethod
    def ReadTrecOut(InName):
        lQid = []
        llDocNo = []
        for line in open(InName):
            vCol = line.strip().split()
            if len(vCol) < 6:
                continue
            qid = vCol[0]
            DocNo = vCol[2]
            if lQid == []:
                lQid.append(qid)
                llDocNo.append([])
            if qid != lQid[len(lQid) - 1]:
                lQid.append(qid)
                llDocNo.append([])
            llDocNo[len(llDocNo) - 1].append(DocNo)
        return lQid,llDocNo
            
    

def AdhocEvaUnitTest(ConfIn = ""):
    #UnitTest add hoc eva
    #input: trec type input + qrel
    #output: evaluation result
    if "" == ConfIn:
        print "conf:\nin\nqrel\nevadepth\nout\n"
        return False
    
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    AdhocEva = AdhocEvaC(ConfIn)
    
    MeanRes = AdhocMeasureC()
    cnt = 0
    
    CurrentQid = ""
    lDocNo = []
    
    out = open(OutName,'w')
    for line in open(InName):
        line = line.strip()
        vCol = line.split()
        ThisQid = vCol[0]
        DocNo = vCol[2]
        if CurrentQid == "":
            CurrentQid = ThisQid
        if CurrentQid != ThisQid:
            EvaRes = AdhocEva.EvaluatePerQ(CurrentQid, lDocNo)
            OutStr = CurrentQid + " %s" %(EvaRes.dumps())
                
            #this is bad
            MeanRes = MeanRes + EvaRes
            cnt += 1
            print >> out, OutStr
            CurrentQid = ThisQid
            lDocNo = []
        lDocNo.append(DocNo)
    EvaRes = AdhocEva.EvaluatePerQ(CurrentQid, lDocNo)
    OutStr = CurrentQid + " %s" %(EvaRes.dumps())                
    MeanRes = MeanRes + EvaRes
    cnt += 1
    print >> out, OutStr    
    
    MeanRes = MeanRes / cnt
    print >> out,"mean %s" %(MeanRes.dumps())
    out.close()    
    return True
    
    
    
    
    
    
    
    