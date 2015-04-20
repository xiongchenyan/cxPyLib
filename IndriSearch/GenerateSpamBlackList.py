'''
Created on Apr 20, 2015 5:24:20 PM
@author: cx

what I do:
I generate to filter out spam list
    for qid, query
        run to index, get docs
    go through spam data, record those to filter
what's my input:
qid query
index
cachedir
spam data
spam range (60 default)
what's my output:

a qid\t docno black list

'''

'''
not in use now.
directly discard spam in index is a much better idea

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
    
    
    



    
        
        
        
        
    
    