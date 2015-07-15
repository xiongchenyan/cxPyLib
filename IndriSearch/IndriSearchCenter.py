'''
Created on Oct 29, 2014 4:04:23 PM
@author: cx

what I do:
I am the center of indri search.
I run query, with a hidden cache center.
    the cache name is defined by query
I will also support SDM query.
what's my input:
query
what's my output:
lDoc
'''
import math

'''
Dec 27 2014
add extract PRF Lm for a query
    first run query get ldoc
    then use RM3 for Lm (need input CtfCenter for idf)
'''

'''
Apr 20 2015
Add func to read ref rank
Add func to filter by OOV  (main focus)
Add func to filter give blacklist Qid-DocNo pairs (not in use for now)

TBD:
    get 60 black list
    build 60 spam filtered index for CW09CatB
    check baseline performance
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import json
from IndriSearch.IndriDocBase import IndriDocBaseC
from IndriRelate.IndriInferencer import LmBaseC
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC
import os
import ntpath
import subprocess
import math
import logging
class IndriSearchCenterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.CacheDir = ""
        self.WriteCache = True
        self.IndexPath = ""
        self.NumOfDoc = 100
        self.OOVFractionFilter = False   #default false
        self.OOVMinFraction = 0.1  #must have >= 0.1 oov to stay
        self.ExecPath = "/bos/usr0/cx/RunQuery/RunQueryJsonOut"
        self.hQRefRank = {}   #{qid->[DocNo,DocScore]}
        self.RefRankInName = ""
        
        self.BlackListInName = ""
        self.hQBlackList = {}   #qid->{DocNo}
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.CacheDir = self.conf.GetConf('cachedir') + '/'
        if not os.path.exists(self.CacheDir):
            os.mkdir(self.CacheDir)
        self.WriteCache = bool(int(self.conf.GetConf('writeindricache',self.WriteCache)))
        self.IndexPath = self.conf.GetConf('indexpath') + '/'
        self.NumOfDoc = int(self.conf.GetConf('numofdoc',self.NumOfDoc))
        self.RefRankInName = self.conf.GetConf('refrank')
        if "" != self.RefRankInName:
            self.LoadRefRank()
            
        self.BlackListInName = self.conf.GetConf('blacklist')
        if "" != self.BlackListInName:
            self.LoadBlackList()
        self.OOVFractionFilter = bool(int(self.conf.GetConf('oovfilter', 0)))
            
            
            
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        print cls.__name__ 
        print 'cachedir\nwriteindricache\nindexpath\nnumofdoc\nrefrank (opt)\nblacklist (opt)'
        print 'oovfilter 0'
            
    def LoadRefRank(self):
        lLines = open(self.RefRankInName).read().splitlines()
        lItem = [line.split() for line in lLines]
        lQidDocScore = [[item[0],item[2],float(item[4])] for item in lItem]
        
        for qid, DocNo,score in lQidDocScore:
            if not qid in self.hQRefRank:
                self.hQRefRank[qid] = [[DocNo,score]]
            else:
                self.hQRefRank[qid].append([DocNo,score])
        logging.info('ref rank loaded from [%s]',self.RefRankInName)        
        return True
        
        
    def LoadBlackList(self):
        '''
        qid\tdocno file
        '''    
        lLines = open(self.BlackListInName).read().splitlines()
        lQidDocNo = [line.split() for line in lLines]
        
        for qid,DocNo in lQidDocNo:
            if not qid in self.hQBlackList:
                self.hQBlackList[qid] = set([DocNo])
            else:
                self.hQBlackList[qid].add(DocNo)
                
        logging.info('load black list from [%s] done',self.BlackListInName)
        return True
            
        
        
    def RunQuery(self,query,qid = ""):
        '''
        must have qid to use ref rank
        '''
        logging.info("indri running query [%s]", query)
        lDoc = []
        TextResult = self.LoadCache(query)
        lMid = []
        if "" != TextResult:
            lMid = json.loads(TextResult)
        if len(lMid) < self.NumOfDoc:
            TextResult = self.CallExec(query)
            if self.WriteCache:
                self.DumpCache(query, TextResult)
            lMid = json.loads(TextResult)
                
        
        for MidDoc in lMid:
            doc = IndriDocBaseC(MidDoc)
            if not self.IsFilterDoc(qid,doc):
                lDoc.append(doc)
        '''
        use ref rank here if qid != "" and qid exists in self.hQRefRank
        '''        
        lDoc = self.FollowRefRank(qid, lDoc)
        logging.info('query [%s][%s] get [%d] doc',qid,query,len(lDoc))
        
        return lDoc[:self.NumOfDoc]
    
    
    def RunQueryTrecEvalFormat(self,query,qid):
        lResStr = []
        lDoc = self.RunQuery(query, qid)
        for i in range(len(lDoc)):
            ResStr = qid + ' Q0 ' + lDoc[i].DocNo + ' %d '%(i + 1) + ' %f IndriBase'%(lDoc[i].score)
            lResStr.append(ResStr)
        return lResStr
        
    
    
    def IsFilterDoc(self,qid,doc):
        
        if self.InBlackList(qid,doc):
            return True
        
        if self.IsSpamDoc(doc):
            return True
        
        return False
    
    
    
    def FollowRefRank(self,qid,lRawDoc):
        '''
        match the qid's [doc,score] ranks,
        order and score modified, till have enough self.NumOfDoc
        '''
        
        if qid == "":
            return lRawDoc
        if not qid in self.hQRefRank:
            return lRawDoc
        
        lDocNoScore = self.hQRefRank[qid]
        
        lModifiedDoc = []
        lDocNoInRaw = [doc.DocNo for doc in lRawDoc]
        hDocP = dict(zip(lDocNoInRaw,range(len(lDocNoInRaw))))
        
        MissCnt = 0
        for DocNo,score in lDocNoScore:
            if not DocNo in hDocP:
                MissCnt += 1
                continue
            doc = lRawDoc[hDocP[DocNo]]
            doc.score = score
            lModifiedDoc.append(doc)
            if len(lModifiedDoc) >= self.NumOfDoc:
                break
        
        if 0 != MissCnt:
            logging.warn('get [%d] doc for qid [%s], missing [%d] doc in ref rank',len(lModifiedDoc),qid,MissCnt)
        else:
            logging.info('qid [%s] ref rank full filled',qid)
        return lModifiedDoc
        
        
        
        
        
    def InBlackList(self,qid,doc):
        if not qid in self.hQBlackList:
            return False
        if not doc.DocNo in self.hQBlackList[qid]:
            return False
        return True    
    
    def IsSpamDoc(self,doc):
        if self.OOVFractionFilter:
            if doc.OOVFraction() < self.OOVMinFraction:
                return True
        return False
        
        
        
    
        
        
    
    
    
    def RM3PRF(self,query,CtfCenter):
        lDoc = self.RunQuery(query)
        hPRFTerm = {}
        for doc in lDoc:
            DocLm = LmBaseC(doc)
            for term in DocLm.hTermTF.keys():
                prob = DocLm.GetTFProb(term)
                score = prob * math.exp(doc.score)
                if not term in hPRFTerm:
                    hPRFTerm[term] = score
                else:
                    hPRFTerm[term] += score
                    
        for term in hPRFTerm.keys():
            LogIDF = CtfCenter.GetLogIdf(term)
            hPRFTerm[term] *= LogIDF
        return hPRFTerm
        
        
    
    
    def GenerateCacheName(self,query):
        return self.CacheDir + '/' +  TextBaseC.DiscardNonAlphaNonDigit(query).replace(" ","_")[:100]
    
    @staticmethod
    def GenerateQueryTargetName(query):
        return TextBaseC.DiscardNonAlphaNonDigit(query).replace(" ","_")[:100]
    
    @staticmethod
    def RearrangeDocOrder(lDoc,lDocNo):
        #stuff in lDocNo must be in lDoc
        lRes = []
        hDocPos = dict(zip([doc.DocNo for doc in lDoc],range(len(lDoc))))
        for DocNo in lDocNo:
            if not DocNo in hDocPos:
                logging.error('doc [%s] not in lDoc given (IndriSearchCenter.RearrageDocOrder)',DocNo)
                sys.exit()
            lRes.append(lDoc[hDocPos[DocNo]])
        return lRes
            
    
    def LoadCache(self,query):
        if self.CacheDir == "":
            return ""
        FName = self.GenerateCacheName(query)
        if not os.path.exists(FName):
            return ""
        lLine = open(FName).readlines()
        return '\n'.join(lLine).replace('\\','')
    
    def DumpCache(self,query,TextResult):
        FName = self.GenerateCacheName(query)
        out = open(FName,'w')
        print >>out, TextResult
    
    def CallExec(self,query):
        logging.info("query[%s] cache not find, running to index",query)
        OutStr = subprocess.check_output([self.ExecPath,query,self.IndexPath])
        line = OutStr.split('\n')[-1]
        line = line.replace('\\','')
        return line
    

'''
add simple run qid\tquery and output trec format function
copied from IndriSearchRunQuery
'''    
if __name__ == "_main__":
    import sys

    if 2 != len(sys.argv):
        IndriSearchCenterC.ShowConf()
        print "in"
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
        
    Searcher = IndriSearchCenterC(sys.argv[1])
    conf = cxConfC(sys.argv[1])
    
    QInName = conf.GetConf('in')
    for line in open(QInName):
        qid,query = line.strip().split('\t')
        Searcher.RunQuery(query,qid)
    
    print "finished"   
   
   
        
        
        



