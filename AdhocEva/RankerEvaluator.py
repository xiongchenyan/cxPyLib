'''
Created on Sep 1, 2015 6:00:18 PM
@author: cx

what I do:
    I evaluate a ranker function
what's my input:
    queries
    IndriSearchCenterC's input
    AdhocEvaC's input
    a function that takes input:
        qid,query,lDoc
        and return lDocNo as reranked results
what's my output:
    the evaluate results of the given ranker

'''

import site
import logging
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from AdhocEva import AdhocEvaC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from AdhocMeasure import AdhocMeasureC

class RankerEvaluatorC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.Searcher = IndriSearchCenterC()
        self.Evaluator = AdhocEvaC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Searcher.SetConf(ConfIn)
        self.Evaluator.SetConf(ConfIn)
        
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        IndriSearchCenterC.ShowConf()
        AdhocEvaC.ShowConf()
        
        
    def Evaluate(self,QIn,Ranker,EvaOut = ""):
        
        lQidQuery = [line.split('\t') for line in open(QIn).read().splitlines()]
        
        lQEvaRes = []
        
        for qid,query in lQidQuery:
            lDoc = self.Searcher.RunQuery(query, qid)
            lReRankDocNo = Ranker(qid,query,lDoc)
            EvaRes = self.Evaluator.EvaluatePerQ(qid, query, lReRankDocNo)
            logging.info('q [%s] res: %s',qid,EvaRes.dumps())
            lQEvaRes.append([qid,EvaRes])
            
        lQEvaRes = AdhocMeasureC.AddMeanEva(lQEvaRes)
        logging.info('mean res: %s',lQEvaRes[-1][1],dumps())
        if EvaOut != "":
            out = open(EvaOut,'w')
            for qid,EvaRes in lQEvaRes:
                print >>out, qid + '\t' + EvaRes.dumps()
            logging.info('evaluated res output to [%s]',EvaOut)
            out.close()
        
        return lQEvaRes
    
    
        



