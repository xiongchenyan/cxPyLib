'''
Created on Dec 9, 2013
unit test for IndriInderencer
@author: cx
'''

import sys
import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
from IndriRelate.IndriInferencer import *

#query, DocInName,CtfInName,OutName

if 5 != len(sys.argv):
    print "4 para: QueryInFile + CashedSERP + CtfFileIn + Out"
    sys.exit()

QueryIn = sys.argv[1]
DocIn = sys.argv[2]
CtfIn = sys.argv[3]
OutName = sys.argv[4]

#flush output
out = open(OutName,'w')
out.close()

for line in open(QueryIn):
    query = line.strip()    
    UnitTest(query, DocIn,CtfIn,OutName)
    
print "finished"
