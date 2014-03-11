'''
Created on Feb 10, 2014
evaluate a rank, by given AdHocQRelC
2/10/2014: MAP supportted
@author: cx
'''
from AdhocQRel import *
import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
from cxBase.base import *
from operator import itemgetter
import math,json
class AdhocEvaC:
    
    def Init(self):
        self.AdhocQRel = AdhocQRelC()
        self.Depth = 20
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return

    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        QRelIn = conf.GetConf("qrel")
        self.AdhocQRel.Load(QRelIn)
        Depth = conf.GetConf("evadepth")
        if "" != Depth:
            self.Depth = int(Depth)
        return True
            
    
    
    def MAP(self,Qid,lDocNo):
        #evaluate the map
        #lDoc is ranked DocNo
        PosCnt = 0
        SumPrecision = 0
        for i in range(min(len(lDocNo),self.Depth)):
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
            print "no rel doc for [%s] best dcg 0" %(qid)
            return 0
        lRelDoc.sort(key=itemgetter(1),reverse=True)
        res = 0
        for i in range(min(len(lRelDoc),self.Depth)):
            res += (math.pow(2.0,lRelDoc[i][1]) - 1) / math.log(1 + i + 1)
        print "[%s] best dcg: [%f]" %(qid,res)
        return res
    
    def DCG(self,qid,lDocNo):
        #calc DCG
        res = 0
        for i in range(min(len(lDocNo),self.Depth)):
            value = self.AdhocQRel.GetScore(qid, lDocNo[i])
            if value == 0:
                continue
            res += (math.pow(2.0,value) - 1) / math.log(1 + i + 1)
        print "[%s] DCG [%f]" %(qid, res)
        return res
    
    def NDCG(self,qid,lDocNo):
        Z = self.BestDCG(qid)
        if 0 == Z:
            return 0
        return self.DCG(qid, lDocNo) / Z
    
    
    
    def PofRel(self,g,gmax):
        return (math.pow(2.0,g) - 1)/math.pow(2.0,gmax)
    
    def ERR(self,qid,lDocNo):
        lRelDoc = self.AdhocQRel.GetAllRelDoc(qid)
        gmax = 0
        for rel in lRelDoc:
            gmax = max(rel[1],gmax)
        
        err = 0
        p = 1
        for i in range(min(len(lDocNo),self.Depth)):
            r = i + 1
            g = self.AdhocQRel.GetScore(qid, lDocNo[i]) 
            R = self.PofRel(g,gmax)
            err += p * R / r
            p = p * (1 - R)
        return err
    
    
    
    def EvaluatePerQ(self,Qid,lDocNo):
        lMeasure = []
        print "start eva query [%s], doc num [%d]" %(Qid,len(lDocNo)) 
        print json.dumps(lDocNo)
        lMeasure.append(["map",self.MAP(Qid, lDocNo)])
        lMeasure.append(['ndcg',self.NDCG(Qid,lDocNo)])
        lMeasure.append(['err',self.ERR(Qid,lDocNo)])
        print "evares:\n%s" %(json.dumps(lMeasure))
        return lMeasure




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
    
    EMAP = 0
    ENDCG = 0
    EERR = 0
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
            lMeasure = AdhocEva.EvaluatePerQ(CurrentQid, lDocNo)
            OutStr = CurrentQid
            for measure in lMeasure:
                OutStr += " %f" %(measure[1])
            #this is bad
            EMAP += lMeasure[0][1]
            ENDCG += lMeasure[1][1]
            EERR += lMeasure[2][1]
            cnt += 1.0
            print >> out, OutStr
            CurrentQid = ThisQid
            lDocNo = []
        lDocNo.append(DocNo)
    lMeasure = AdhocEva.EvaluatePerQ(CurrentQid, lDocNo)
    OutStr = CurrentQid
    for measure in lMeasure:
        OutStr += " %f" %(measure[1])
    #this is bad
    EMAP += lMeasure[0][1]
    ENDCG += lMeasure[1][1]
    EERR += lMeasure[2][1]
    cnt += 1.0
    print >> out, OutStr
    
    
    EMAP /= cnt
    ENDCG /= cnt
    EERR /= cnt
    print >> out,"mean %f %f %f\n" %(EMAP,ENDCG,EERR)
    out.close()
    
    return True
    
    
    
    
    
    
    
    