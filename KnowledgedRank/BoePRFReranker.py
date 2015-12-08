'''
Created on Dec 7, 2015 7:24:56 PM
@author: cx

what I do:
    I rerank doc in the BOE space
    with simple PRF re-ranking
what's my input:
    doc with hEntity
what's my output:
    evaluation results


'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import logging,json
import math

from KnowledgedRank.BoeReranker import *

class BoePRFRerankerC(BoeLmRankerC):
    
    def Init(self):
        BoeLmRankerC.Init(self)
        self.WOrigQ = 0.5
        self.NumOfExpEntity = 20
        
    
    def SetConf(self, ConfIn):
        BoeLmRankerC.SetConf(self, ConfIn)
        self.WOrigQ = float(self.conf.GetConf('wrigq', self.WOrigQ))
        self.NumOfExpEntity = int(self.conf.GetConf('numofexp', self.NumOfExpEntity))
        
        
    @staticmethod
    def ShowConf():
        BoeLmRankerC.ShowConf()
        print 'wrigq=0.5\nnumofexp=20'
        
        
    def QExp(self,qid,query,lDoc):
        hEntityScore = {} #ObjId -> prf score
        for doc in lDoc:
            hDocEntity = self.hDocKg[doc.DocNo]
            for ObjId,score in hDocEntity.items():
                score += doc.score #log(a) + log(b)
                if not ObjId in hEntityScore:
                    hEntityScore[ObjId] = math.exp(score)
                else:
                    hEntityScore[ObjId] += math.exp(score)
        lEntityScore = hEntityScore.items()
        lEntityScore.sort(key=lambda item:item[1])
        lEntityScore = lEntityScore[:self.NumOfExpEntity]
        logging.info(
                     '[%s][%s] exp entity: %s',
                     qid,
                     query,
                     json.dumps(lEntityScore)
                     )
        
        return lEntityScore
    
    def RankScoreForDoc(self,lQObjScore,doc):
        hDocEntity = self.hDocKg[doc.DocNo]

        score = 0
        for ObjId,weight in lQObjScore:
            ObjScore = self.Inferencer.inference(ObjId, hDocEntity)
            score += ObjScore * weight
#             logging.info('[%s] [%s] - [%s] obj score: %f',qid,doc.DocNo,ObjId,ObjScore)
        
#         logging.info('[%s] [%s] ranking score: %f',qid,doc.DocNo,score)
        return score
        
    
    def Rank(self, qid, query, lDoc):
        lQObj = []
        if qid in self.hQObj:
            lQObj = self.hQObj[qid]
        
        lExpEntityScore = self.QExp(qid, query, lDoc)
        
        lQExpObjScore = [[ObjId,self.WOrigQ * score] for ObjId,score in lQObj]
        lQExpObjScore += [
                          [ObjId,score * (1.0 - self.WOrigQ)] 
                          for ObjId,score in lExpEntityScore
                          ]
        lScore = [self.RankScoreForDoc(lQExpObjScore, doc) for doc in lDoc]
        lMid = zip(lDoc,lScore)
        lDocNoScore = [[item[0].DocNo,item[1],item[0].score] for item in lMid]
        #sort doc by two keys, if boe scores tie, use original ranking score
        lDocNoScore.sort(key=lambda item: (item[1],item[2]), reverse = True)
        
        lRankRes = [item[0] for item in lDocNoScore]
        return lRankRes
        
        
        
if __name__=='__main__':
    import sys,os
    from AdhocEva.RankerEvaluator import RankerEvaluatorC
    if 2 != len(sys.argv):
        print 'I evaluate Boe exp model '
        print 'in\nout'
        BoePRFRerankerC.ShowConf()
        RankerEvaluatorC.ShowConf()
        
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    
    
    conf = cxConfC(sys.argv[1])   
    QIn = conf.GetConf('in')
    EvaOut = conf.GetConf('out')
    
    Ranker = BoePRFRerankerC(sys.argv[1])
    Evaluator = RankerEvaluatorC(sys.argv[1])
    Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)        
            
