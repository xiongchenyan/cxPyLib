'''
Created on Mar 11, 2014
ad hoc ranking measure
@author: cx
'''
from operator import itemgetter
class AdhocMeasureC:
    
    def Init(self):
        self.map = 0
        self.ndcg = 0
        self.err = 0
        return
    
    
    def __init__(self,line =""):
        self.Init()
        if "" != line:
            self.loads(line)
        
        
    def __deepcopy__(self,memo):
        res = AdhocMeasureC()
        res.map = self.map
        res.ndcg = self.ndcg
        res.err = self.err
        return res
    
    def __add__(self,other):
        res = AdhocMeasureC()
        res.map = self.map + other.map
        res.ndcg = self.ndcg + other.ndcg
        res.err = self.err + other.err
        return res
    def __div__(self,other):
        res = AdhocMeasureC()
        res.map = self.map / other
        res.ndcg = self.ndcg / other
        res.err = self.err / other
        return res
    
    
    def dumps(self,WithName = False):
        if WithName:
            res = "map:%f ndcg:%f err:%f" %(self.map,self.ndcg,self.err)
        else:
            res = "%f %f %f" %(self.map,self.ndcg,self.err)
        return res
    def loads(self,line,WithName = False):
        vCol = line.strip().split()
        if len(vCol) >= 3:            
            if WithName:
                self.map = float(vCol[0].split(':')[1])
                self.ndcg = float(vCol[1].split(':')[1])
                self.err = float(vCol[2].split(':')[1])
            else:
                self.map = float(vCol[0])
                self.ndcg = float(vCol[1])
                self.err = float(vCol[2])
        return True
            
            

def AdhocMeasureSum(lMeasure):
    Measure = AdhocMeasureC()
    for mid in lMeasure:
        Measure += mid
    return Measure

def AdhocMeasureMean(lMeasure):
    return AdhocMeasureSum(lMeasure) / float(len(lMeasure))
        
        

def AdhocMeasureMatrixSum(llMeasure,Dim = 1):
    if Dim == 1:
        lMeasure = AdhocMeasureMatrixSumOne(llMeasure)
    if Dim == 2:
        lMeasure = AdhocMeasureMatrixSumTwo(llMeasure)    
    return lMeasure


def AdhocMeasureMatrixMean(llMeasure,Dim = 1):
    lSum = AdhocMeasureMatrixSum(llMeasure)
    if Dim == 1:
        Z = float(len(llMeasure))
    if Dim == 2:
        Z = float(len(llMeasure[0]))
    for i in len(lSum):
        lSum[i] /= Z        
    return lSum
        


def AdhocMeasureMatrixSumOne(llMeasure):
    if len(llMeasure) == 0:
        return []
    lRes = []
    for lMeasure in llMeasure:
        if [] == lRes:
            lRes = list(lMeasure)
        else:
            for i in range(len(lRes)):
                lRes[i] += lMeasure[i]
    return lRes

def AdhocMeasureMatrixSumTwo(llMeasure):
    if len(llMeasure) == 0:
        return []
    
    lRes = [AdhocMeasureC()] & len(llMeasure)
    for i in range(len(llMeasure)):
        for j in range(len(llMeasure[i])):
            lRes[i] += llMeasure[i][j]
    return lRes[i]
            

def GetBestPerform(lMeasure,MeasureName='map'):
    if [] == lMeasure:
        return -1
    BestP = 0
    for i in range(len(lMeasure)):
        if getattr(lMeasure[i],MeasureName) > getattr(lMeasure[BestP],MeasureName):
            BestP = i
    return BestP



def ReadPerQEva(InName):
    lPerQEva = []
    for line in open(InName):
        line = line.strip()
        qid,MeaStr = line.split('\t')
        if qid == 'mean':
            continue
        qid = int(qid)
        Measure = AdhocMeasureC(MeaStr)
        lPerQEva.append([qid,Measure])
    lPerQEva.sort(key=itemgetter(0))
    return lPerQEva
    
    
        
    
         