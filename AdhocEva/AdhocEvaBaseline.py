'''
Created on Jul 22, 2014
evaluate the base line results
input: Cash Dir (Indri, or SDM) + conf of AdhocEvaC
output: evaluation file
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from AdhocEva import *
from IndriRelate.IndriPackedRes import *
from cxBase.Conf import cxConfC



def EvaluatePerQ(qid,query,Evaluator,CashDir):
    lDoc = ReadPackedIndriRes(CashDir + '/' + query)
    lDocNo = [Doc.DocNo for Doc in lDoc]
    Measure = Evaluator.EvaluatePerQ(qid,lDocNo)
    return Measure


import sys

if 2 != len(sys.argv):
    print "conf:"
    print "cashdir\nin\nout"
    AdhocEvaC.ShowConf()
    sys.exit()
    
Evaluator = AdhocEvaC(sys.argv[1])
conf = cxConfC(sys.argv[1])

QueryIn = conf.GetConf('in')
OutName = conf.GetConf('out')
CashDir = conf.GetConf('cashdir')

out = open(OutName,'w')
for line in open(QueryIn):
    qid,query = line.strip().split('\t')
    Measure = EvaluatePerQ(qid,query,Evaluator,CashDir)
    print >>out, qid + '\t' + Measure.dumps()
out.close() 