'''
Created on Dec 24, 2014 1:23:57 PM
@author: cx

what I do:
I make baseline evaluation results
using IndriSearch Package
current unsupervised baselines:
    lm
    sdm
what's my input:
qid\tquery
index
cachedir
what's my output:
evaluation results

'''

import site
from cxBase.Conf import cxConfC
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.QueryGenerator import QueryGeneratorC

import sys


def EvaluatePerQ(qid,query,Searcher,Evaluator):
    lDoc = Searcher.RunQuery(query)
    lDocNo = [Doc.DocNo for Doc in lDoc]
    Measure = Evaluator.EvaluatePerQ(qid,lDocNo)
    return Measure

def ReadAndGenerateQuery(InName,QueryType = 'raw'):
    lLine = open(InName).read().splitlines()
    lQidQuery = [line.split('\t') for line in lLine]
    if QueryType == 'sdm':
        lQidQuery = [[qid,QueryGeneratorC.GenerateSDM(query)] for qid,query in lQidQuery]
    return lQidQuery


if 2 != len(sys.argv):
    IndriSearchCenterC.ShowConf()
    AdhocEvaC.ShowConf()
    print "in\nout\nquerytype raw|sdm"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
QType = conf.GetConf('querytype')
Searcher = IndriSearchCenterC(sys.argv[1])
Evaluator = AdhocEvaC(sys.argv[1])

lQidQuery = ReadAndGenerateQuery(InName, QType)

lMeasure = [EvaluatePerQ(qid, query, Searcher, Evaluator) for qid,query in lQidQuery]

Mean = AdhocMeasureC.AdhocMeasureMean(lMeasure)

out = open(OutName,'w')

for i in range(len(lMeasure)):
    print >>out,lQidQuery[i][0] + '\t' + lMeasure[i].dumps()
    
print >>out, 'mean\t' + Mean.dumps()

out.close()
print "finished"