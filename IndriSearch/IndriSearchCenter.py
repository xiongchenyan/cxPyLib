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
class IndriSearchCenterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.CacheDir = ""
        self.WriteCache = True
        self.IndexPath = ""
        self.NumOfDoc = 100
        self.ExecPath = "/bos/usr0/cx/RunQuery/RunQueryJsonOut"
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.CacheDir = self.conf.GetConf('cachedir') + '/'
        self.WriteCache = bool(int(self.conf.GetConf('writeindricache',self.WriteCache)))
        self.IndexPath = self.conf.GetConf('indexpath') + '/'
        self.NumOfDoc = int(self.conf.GetConf('numofdoc',self.NumOfDoc))
        
        
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'cachedir\nwriteindricache\nindexpath\nnumofdoc'
        
        
    def RunQuery(self,query):
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
        for MidDoc in lMid[:self.NumOfDoc]:
            doc = IndriDocBaseC(MidDoc)
            lDoc.append(doc)
        return lDoc;
    
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
        return self.CacheDir + TextBaseC.DiscardNonAlphaNonDigit(query).replace(" ","_")[:100]
    
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
    
    
        
        
        



