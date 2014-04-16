'''
Created on Apr 16, 2014
input: a q-exp term lExpTerm
do: form a para file, call indrirunquery, get trec result, evaluate
output: evaluation result
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriRelate.IndriQueryParameter import *
import subprocess
from CondorBase import *
import json


from cxBase.base import *
from AdhocEva.AdhocEva import *


RunQueryExe = '/bos/usr0/cx/RunQuery/RunQuery'

class IndriRankerC(cxBaseC):
    def Init(self):
        self.IndexDir = "/bos/tmp17/gzheng/ClueWeb09_Indexes_Spam_Filtered/ClueWeb09_English_01"
        self.NumOfRes = 20
        self.NeedEva = True
        self.Evaluator = AdhocEvaC()
        
        self.InQuery = ""
        self.OutDir = "" #will out: reranked doc id (trec format) + evaluation result
        
        
    def SetConf(self,ConfIn):
        self.Evaluator.SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.IndexDir = conf.GetConf('index', self.IndexDir)
        self.NumOfRes = conf.GetConf('numofres',self.NumOfRes)
        self.NeedEva = conf.GetConf('needeva',self.NeedEva)
        self.InQExp = conf.GetConf('in')
        self.OutDir = conf.GetConf('outdir')
        return True
    
    
    @staticmethod
    def ShowConf():
        print"index /bos/tmp17/gzheng/ClueWeb09_Indexes_Spam_Filtered/ClueWeb09_English_01\nnumofres 20\nneedeve True\nin\noutdir" 
    
    
    def Process(self):
        #read query
        #form a q para file
        #call run query, fetch result
        #evaluate
        
        
        lQid = []
        lQuery = []
        
        for line in open(self.InQuery):
            qid,query = line.strip().split('\t')
            lQid.append(qid)
            lQuery.append(query)
        
        self.MakeQParaFile(lQid, lQuery)
        
        ReRankOutStr = subprocess.check_output(RunQueryExe,self.QueryParaName())
        
        OutReRank = open(self.OutRerankName(),'w')
        print >> OutReRank, ReRankOutStr
        OutReRank.close()
        
        if self.NeedEva:
            self.Evaluator.EvaluateTrecOutFile(self.OutRerankName(), self.OutEvaName()) 
        
        return True
    


        
    def MakeQParaFile(self,lQid,lQuery):
        IndriPara = IndriQueryParaC()
        IndriPara.SetField('index', self.IndexDir)
        IndriPara.SetField('count','%s' %(self.NumOfRes))
        IndriPara.SetField('rule','method:dir')
        IndriPara.SetField('trecFormat','1')
        IndriPara.SetQueryPara('type', 'indri')
        
        
        for i in range(len(lQid)):
            IndriPara.AddQuery(lQuery[i], lQid[i])
            
        IndriPara.Dump(self.QueryParaName())
        return True
        
        
        
        
    def QueryParaName(self):
        return self.OutDir + "/QPara"    
        
    
    def OutRerankName(self):
        return self.OutDir + "/ranking"
    

    
    def OutEvaName(self):
        return self.OutDir + "/eva"
        
