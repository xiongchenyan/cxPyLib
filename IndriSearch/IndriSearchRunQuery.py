'''
Created on Dec 16, 2014 8:44:56 PM
@author: cx

what I do:
I run query using IndriSearchCenter
The goal is to transfer the old IndriRelate to IndriSearch
what's my input:
qid\tquery
what's my output:
to the cache dir

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from cxBase.Conf import cxConfC
import sys

if 2 != len(sys.argv):
    IndriSearchCenterC.ShowConf()
    print "in"
    sys.exit()
    
Searcher = IndriSearchCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])

QInName = conf.GetConf('in')
for line in open(QInName):
    qid,query = line.strip().split('\t')
    Searcher.RunQuery(query,qid)

print "finished"