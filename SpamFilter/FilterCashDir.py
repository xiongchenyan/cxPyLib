'''
Created on Jul 16, 2014
filter spams in a cash dir
in: cash dir + query list + spam score file
output: out cash dir, spam filtered
@author: chenyan
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')

from cxBase.Conf import cxConfC
from IndriRelate.IndriPackedRes import *

def LoadTargetDocId(CashDir, QueryIn):
    hTargetDocId = {}
    for line in open(QueryIn):
        query = line.strip().split('\t')[1]
        lDoc = ReadPackedIndriRes(CashDir + '/' + query)
        for Doc in lDoc:
            hTargetDocId[Doc.DocNo] = True
    print "load [%d] target doc id" %(len(hTargetDocId))        
    return hTargetDocId

def FilterBySpamScore(SpamIn,hDocId,SpamBar = 50):
    print 'start filter'
    cnt = 0
    for line in open(SpamIn):
        cnt += 1
        if 0 == (cnt % 10000):
            print "processed [%d] spam scores" %(cnt)
        score,DocNo = line.strip().split()
        score = int(score)
        if score >= SpamBar:
            continue
        if DocNo in hDocId:
            del hDocId[DocNo]
    print "keep [%d] doc id" %(hDocId)
    return hDocId

def FilterCache(CashDir,OutDir,QueryIn,QueryOut,hKeepDocId):
    hQid = {}
    for line in open(QueryOut):
        qid,query= line.strip().split('\t')
        hQid[qid] = query
        
    for line in open(QueryIn):
        qid,query = line.strip().split('\t')
        lDoc = ReadPackedIndriRes(CashDir + '/' + query)
        out = open(OutDir + '/' + hQid[qid],'w')
        for Doc in lDoc:
            if Doc.DocNo in hKeepDocId:
                print >>out, Doc.dumps()
        out.close()
        print "[%s] done" %(hQid[qid])
    print "filter cache done"
        
import sys
if 2 != len(sys.argv):
    print "conf:"
    print "cashdir\noutdir\nqueryin\nqueryout\nspamfile\nspamscore 50"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
CashDir = conf.GetConf('cashdir')
OutDir = conf.GetConf('outdir')
QueryIn = conf.GetConf('queryin')
QueryOut = conf.GetConf('queryout')
SpamIn = conf.GetConf('spamfile')
SpamBar = conf.GetConf('spamscore',50)

hAllDoc = LoadTargetDocId(CashDir,QueryIn)   
hKeepDoc = FilterBySpamScore(SpamIn,hAllDoc,SpamBar)
FilterCache(CashDir,OutDir,QueryIn,QueryOut,hKeepDoc)
    
    
    