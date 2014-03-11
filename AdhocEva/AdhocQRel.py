'''
Created on Feb 10, 2014
QRel Center
@author: cx
'''

import sys


class AdhocQRelC:
    def Init(self):
        self.hQRel = {}
        self.hQToDoc={} #query to documents
        self.MaxScore = 0
        return
    def __init__(self):
        self.Init()
    def Load(self,InName):
        #key: qid\tdocid
        #value:score, 0 if not contained
        for line in open(InName):
            vCol = line.strip().split()
            qid = vCol[0]
            DocId = vCol[2]
            value = int(vCol[3])
            if 0 == value:
                continue
            self.hQRel[qid + "\t"+ DocId] = value
            self.MaxScore = max(self.MaxScore,value)
            if not qid in self.hQToDoc:
                self.hQToDoc[qid] = []
            self.hQToDoc[qid].append([DocId,value])
        return True
    
    def GetScore(self,qid,docid):
        key = qid + "\t" + docid
        if not key in self.hQRel:
            return 0
        return self.hQRel[key]
    
    def GetAllRelDoc(self,qid):
        if not qid in self.hQToDoc:
            return []
        return self.hQToDoc[qid]
