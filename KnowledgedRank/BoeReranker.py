'''
Created on Nov 23, 2015 5:49:40 PM
@author: cx

what I do:
    I rerank indri search results via doc's query entity score's
what's my input:
    query,
    retrieved docs
    query entities
    doc's entity-score
what's my output:
    evaluation results

'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import logging,json
import math


class BoeLmC(object):
    def __init__(self,Normilize = False):
        self.Init(Normilize)
        
    def Init(self,Normilize = False):
        self.MinWeight = -20
        self.Normilize = Normilize
        return
    
    
    def inference(self,ObjId,hDocEntity,doc):
        '''
        return the log prob if p(ObjId| DocKg)
        '''
        
        score = self.MinWeight
        
        if self.Normilize:
            Z = sum([math.exp(item[1]) for item in hDocEntity.items()])
            Z = max(Z, math.exp(self.MinWeight))
            Z = math.log(Z)
        
        return sum([math.exp(item[1]) for item in hDocEntity.items()])
        
        if ObjId in hDocEntity:
            score = hDocEntity[ObjId]
#             score = 1
            if self.Normilize:
#                 score += Z
                score -= math.log(float(len(doc.lPosition)))
                
        return score


class BoeLmRankerC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.hQObj = {}
        self.hDocKg = {}  #docNo->{obj:score}
        self.Inferencer = BoeLmC()
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        DocEntityIn = self.conf.GetConf('dockgin')
        QAnaInName = self.conf.GetConf('qanain')
        
        self.LoadQObj(QAnaInName)
        self.LoadDocObj(DocEntityIn)
        self.SetInferencer()
        self.Normalize = False
        
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'dockgin\nqanain\nnormalize'
        
    
    def SetInferencer(self):
        self.Normalize = bool(self.conf.GetConf('normalize', 0))
        self.Inferencer = BoeLmC(self.Normalize)
        return
            
    
    def LoadQObj(self,QAnaInName):
        for line in open(QAnaInName).read().splitlines():
            vCol = line.strip().split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = float(vCol[-1])
            if not qid in self.hQObj:
                self.hQObj[qid] = [[ObjId,score]]
            else:
                self.hQObj[qid].append([ObjId,score])
                
        logging.info('qobj loaded from [%s]',QAnaInName)
        return True
    
    def LoadDocObj(self,DocEntityIn):
        for line in open(DocEntityIn):
            DocNo,EStr = line.strip().split('\t')
            hDocEntity = json.loads(EStr)
            self.hDocKg[DocNo] = hDocEntity
        logging.info('doc kg loaded from [%s]',DocEntityIn)
    
    
    def RankScoreForDoc(self,qid,doc):
        if not doc.DocNo in self.hDocKg:
            return self.Inferencer.MinWeight
        
        lQObj = self.hQObj[qid]
        hDocEntity = self.hDocKg[doc.DocNo]

        score = 0
        for ObjId,weight in lQObj:
            ObjScore = self.Inferencer.inference(ObjId, hDocEntity,doc)
            score += ObjScore * weight
            logging.info('[%s] [%s] - [%s] obj score: %f',qid,doc.DocNo,ObjId,ObjScore)
        
        logging.info('[%s] [%s] ranking score: %f',qid,doc.DocNo,score)
        return score
    
    def Rank(self,qid,query,lDoc):
        if not qid in self.hQObj:
            logging.warn('qid [%s] no ana obj, withdraw to given score',qid)
            return [doc.DocNo for doc in lDoc]
        
        lScore = [self.RankScoreForDoc(qid, doc) for doc in lDoc]
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
        print 'I evaluate Boe model '
        print 'in\nout'
        BoeLmRankerC.ShowConf()
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
    
    Ranker = BoeLmRankerC(sys.argv[1])
    Evaluator = RankerEvaluatorC(sys.argv[1])
    Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)
     
    
        
        
        
        
        
            
            
        
        




