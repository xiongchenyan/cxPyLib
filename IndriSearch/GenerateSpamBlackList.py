'''
Created on my MAC Apr 20, 2015-6:06:09 PM
What I do:

What's my input:

What's my output:

@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.QueryGenerator import QueryGeneratorC

import sys
import logging

FilterPercent = 60



def FormQidDocList(QueryInName,Searcher):
    lLines = open(QueryInName).read().splitlines()
    lQidQuery = [line.split('\t') for line in lLines]
    
    hQidDoc = {}
    for qid,query in lQidQuery:
        hQidDoc[qid] = Searcher.RunQuery(query,qid)
        
    return hQidDoc


def FormBlackDocNo(SpamInName,hQidDoc):
    sDocNo = set()
    for key,item in hQidDoc.items():
        sDocNo.update([doc.DocNo for doc in item])
    
    sBlackDocNo =set()    
    global FilterPercent
    for line in open(SpamInName):
        DocNo,score = line.strip().split()
        score = float(score)
        if score >= FilterPercent:
            continue
        if DocNo in sDocNo:
            sBlackDocNo.add(DocNo)
    return sBlackDocNo


def DumpQidBlackDocNo(hQidDoc,sBlackDocNo,OutName):
    
    return True
    
    
    



    
        
        
        
        
    
    