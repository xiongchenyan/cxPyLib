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

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import json
from IndriSearch.IndriDocBase import IndriDocBaseC
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC
import os
import ntpath
import subprocess

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
        if "" == TextResult:
            TextResult = self.CallExec(query)
            if self.WriteCache:
                self.DumpCache(query, TextResult)
        lMid = json.loads(TextResult)
        for MidDoc in lMid[:self.NumOfDoc]:
            doc = IndriDocBaseC()
            doc.__dict__ = MidDoc
            lDoc.append(doc)
        return lDoc;
    
    
    def GenerateCacheName(self,query):
        return self.CacheDir + TextBaseC.DiscardNonAlphaNonDigit(query).replace(" ","_")[:100]
    
    def LoadCache(self,query):
        FName = self.GenerateCacheName(query)
        if not os.path.exists(FName):
            return ""
        lLine = open(FName).readlines()
        return '\n'.join(lLine)
    
    def DumpCache(self,query,TextResult):
        FName = self.GenerateCacheName(query)
        out = open(FName,'w')
        print >>out, TextResult
    
    def CallExec(self,query):
        print "query[%s] cache not find, running to index" %(query)
        OutStr = subprocess.check_output([self.ExecPath,query,self.IndexPath])
        line = OutStr.split('\n')[-1]
        return line
    
    
        
        
        



