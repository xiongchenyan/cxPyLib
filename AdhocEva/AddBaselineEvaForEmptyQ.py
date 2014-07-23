'''
Created on Jul 23, 2014
add baseline evaluation results for empty q
input: target eva + base line eva + output
out: target eva, added with baseline
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')

from AdhocMeasure import *

import sys

if 4 != len(sys.argv):
    print "add baseline's eva to target eva"
    print "3 para:target eva + base eva + out"
    sys.exit()
    
    
lPerQEva = AdhocMeasureC.ReadPerQEva(sys.argv[1], True)
lBaseEva = AdhocMeasureC.ReadPerQEva(sys.argv[2],True)

lNewQEva = AdhocMeasureC.FillMissEvaByBaseline(lPerQEva, lBaseEva)


AdhocMeasureC.DumpPerQEva(sys.argv[3], lNewQEva)
