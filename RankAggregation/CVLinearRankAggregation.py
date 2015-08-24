'''
Created on Aug 24, 2015 3:29:06 PM
@author: cx

what I do:
    train part (for linear weight lambda)
what's my input:
    original rank + parastr + eva res
what's my output:


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from sklearn.cross_validation import KFold

from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC

import logging

class CVLinearRankAggregationC(cxBaseC):
    def Init(self):
        self.Evaluator = AdhocEvaC()
        self.RankInName = ""
        self.MergeInName = ""
        self.lLambda = [0.1 * i for i in range(11)]
        self.OutName = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Evaluator.SetConf(ConfIn)
        self.RankInName = self.conf.GetConf('in')
        self.MergeInName = self.conf.GetConf('tomergein')
#         self.Lambda = self.conf.GetConf('lambda', self.Lambda)
        self.OutName = self.conf.GetConf('out')
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'in\ntomergein\nout'
        
        
    def ReadRankingScore(self,InName):
        
        lLines = open(InName).read().splitlines()
        lvCol = [line.split()  for line in lLines]
        lQidDocScore = [[vCol[0],vCol[2],float(vCol[4])] for vCol in lvCol]
        
        MaxScore = max([item[2] for item in lQidDocScore])
        MinScore = min([item[2] for item in lQidDocScore])
        
        lQidDocScore = [[item[0],item[1],(item[2] - MinScore )/ (MaxScore - MinScore)] for item in lQidDocScore]
        
        logging.info('ranking res loadded from [%s]',InName)
        return lQidDocScore
    
    
    def MergeTwoRank(self,lQidDocScoreA,lQidDocScoreB,Lambda):
        lKeyB = [item[0] + '\t' + item[1] for item in lQidDocScoreB]
        lScoreB = [item[2] for item[2] in lQidDocScoreB]
        
        hB = dict(zip(lKeyB,lScoreB))
        
        lNewQidDocScore = []
        for qid,doc,score in lQidDocScoreA:
            ToAdd = 0
            key = qid + '\t' + doc
            if key in hB:
                ToAdd = hB[key]
            score = (1- Lambda) * score + Lambda * ToAdd
            lNewQidDocScore.append([qid,doc,score])
            
        return lNewQidDocScore
    
    
    def EvaluateRank(self,lQidDocScore):
        lEvaRes = []
        
        lDocScore = []
        LastQid = lQidDocScore[0][0]
        lQid = []
        for qid,doc,score in lQidDocScore:
            
            if qid != LastQid:
                lDocScore.sort(key = lambda item:item[1],reverse = True)
                lDocNo = [item[0] for item in lDocScore]
                EvaRes = self.Evaluator.EvaluatePerQ(LastQid, "", lDocNo)
#                 logging.info('EvaRes [%s]: %f',LastQid,EvaRes.dumps())
                lEvaRes.append(EvaRes)
                lQid.append(LastQid)
                lDocScore = []
                LastQid = qid
            
            lDocScore.append([doc,score])
        lDocScore.sort(key = lambda item:item[1],reverse = True)
        lDocNo = [item[0] for item in lDocScore]
        EvaRes = self.Evaluator.EvaluatePerQ(LastQid, "", lDocNo)
        lEvaRes.append(EvaRes)
        lDocScore = []
        
        
        return lQid,lEvaRes
    
    def FindBestLambda(self,lTrainData,lMergeData):
        BestErr = 0
        BestLambda = 0
        
        for Lambda in self.lLambda:
            lEvaRes = self.TestLambda(lTrainData, lMergeData, Lambda)[1]
            MeanRes = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
            if MeanRes.err > BestErr:
                logging.info('better lambda [%f] err [%f]',Lambda,MeanRes.err)
                BestErr = MeanRes.err
                BestLambda = Lambda
                
        return BestLambda
            
        
    
    def RunOneFold(self,lTrainQidDocScoreA,lTestQidDocScoreA,lQidDocScoreB):
        
        Lambda = self.FindBestLambda(lTrainQidDocScoreA,lQidDocScoreB)
        logging.info('best lambda in train [%f]',Lambda)
        return self.TestLambda(lTestQidDocScoreA, lQidDocScoreB, Lambda)
    
    def TestLambda(self,lTrainData, lMergeData, Lambda):
        lMergeRes = self.MergeTwoRank(lTrainData, lMergeData, Lambda)
        
        return self.EvaluateRank(lMergeRes)
    
    
    def PartitionRank(self,lQidDocScore):
        
        lQid = list(set([item[0] for item in lQidDocScore]))
        
        llTrainData = []
        llTestData = []
        for train,test in KFold(len(lQid),n_folds = 5):
            lTrainQid = [lQid[i] for i in train]
            lTestQid = [lQid[i] for i in test]
            sTrain = set(lTrainQid)
            sTest = set(lTestQid)
            
            lTrainData = [item for item in lQidDocScore if item[0] in sTrain]
            lTestData = [item for item in lQidDocScore if item[0] in sTest]
            
            llTrainData.append(lTrainData)
            llTestData.append(lTestData)
            
        return llTrainData,llTestData
    
    
    def Process(self):
        
        lQidDocScoreOrig = self.ReadRankingScore(self.RankInName)
        lQidDocScoreMerge = self.ReadRankingScore(self.MergeInName)
        
        
        llTrainData,llTestData = self.PartitionRank(lQidDocScoreOrig)
        
        lEvaRes = []
        lQid = []
        for i in range(len(llTrainData)):
            logging.info('start fold [%d]',i)
            lThisQid,lThisRes = self.RunOneFold(llTrainData[i], llTestData[i], lQidDocScoreMerge)
            lQid.extend(lThisQid)
            lEvaRes.extend(lThisRes)
            
        MeanRes = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        logging.info('res: %s',MeanRes.dumps())
        
        return True
        
        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I linear merge two ranking score list (trec format) using CV'
        print 'conf'
        CVLinearRankAggregationC.ShowConf()
        sys.exit()
        
    Merger = CVLinearRankAggregationC(sys.argv[1])
    Merger.Process()
            
        
        
        
        
        
            
            
            
            
            
    
    
    
        
            
        
            
        
        
        
    