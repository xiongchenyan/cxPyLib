'''
Created on Jun 3, 2014
evaluation results - base line results
in: eva file (trec_eval) - baseline
out: score minus baseline's
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/cxPylib')
from AdhocEva.AdhocMeasure import *

import sys
if 4 != len(sys.argv):
    print "3 para: eva res + base line res + output"
    sys.exit()
    
    
lBasePerQEva = AdhocMeasureC().ReadPerQEva(sys.argv[2],True)
lThisPerQEva = AdhocMeasureC().ReadPerQEva(sys.argv[1],True)


hBaseRes = dict(lBasePerQEva)

out = open(sys.argv[3],'w')

for qid,Measure in lThisPerQEva:
    BlMeasure = hBaseRes[qid]
    Measure -= BlMeasure
    print >> out, "%s\t%s" %(str(qid),Measure.dumps())
    
out.close()