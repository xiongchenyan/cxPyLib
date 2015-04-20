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
            
        
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'cachedir\nwriteindricache\nindexpath\nnumofdoc\nrefrank (opt)'
        
        
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
        
        
        
        
        
    def RunQuery(self,query,qid = ""):
        '''
        must have qid to use ref rank
        '''
        print "running [%s]" %(query)
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
                
#         lMid = [doc for doc in lMid if not self.IsSpamDoc(doc)]
        
        
#         lMid = self.FollowRefRank(qid,lMid)
        
        
        for MidDoc in lMid:
            doc = IndriDocBaseC(MidDoc)
            if not self.IsSpamDoc(doc):
                lDoc.append(doc)
        '''
        use ref rank here if qid != "" and qid exists in self.hQRefRank
        '''        
        lDoc = self.FollowRefRank(qid, lDoc)
        return lDoc[:self.NumOfDoc];
    
    
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
    
    def LoadCache(self,query):
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
        print "query[%s] cache not find, running to index" %(query)
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
   
   
        
        
        



