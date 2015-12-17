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
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.QueryGenerator import QueryGeneratorC

import sys
import logging

def EvaluatePerQ(qid,query,Searcher,Evaluator):
    lDoc = Searcher.RunQuery(query,qid)
    lDocNo = [Doc.DocNo for Doc in lDoc]
    Measure = Evaluator.EvaluatePerQ(qid,query,lDocNo)
    return Measure,lDoc

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

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
QType = conf.GetConf('querytype')
Searcher = IndriSearchCenterC(sys.argv[1])
Evaluator = AdhocEvaC(sys.argv[1])

lQidQuery = ReadAndGenerateQuery(InName, QType)

lMeasureDoc = [EvaluatePerQ(qid, query, Searcher, Evaluator) for qid,query in lQidQuery]

lMeasure = [item[0] for item in lMeasureDoc]
llDoc = [item[1] for item in lMeasureDoc]

Mean = AdhocMeasureC.AdhocMeasureMean(lMeasure)

out = open(OutName,'w')

for i in range(len(lMeasure)):
    print >>out,lQidQuery[i][0] + '\t' + lMeasure[i].dumps()

print 'mean\t' + Mean.dumps()    
print >>out, 'mean\t' + Mean.dumps()

out.close()

RankOut = open(OutName+'_rank','w')
for QidQuery,lDoc in zip(lQidQuery,llDoc):
    qid = QidQuery[0]
    for i in range(len(lDoc)):
        print >> RankOut, qid + ' Q0 ' + lDoc[i].DocNo + ' %d %f indri'%(i+1,lDoc[i].score)
    
RankOut.close()

DocTextOut = open(OutName + '_text','w')
for lDoc in llDoc:
    for doc in lDoc:
        print >>DocTextOut, doc.DocNo + '\t' + doc.GetContent()

DocTextOut.close()
print "finished"