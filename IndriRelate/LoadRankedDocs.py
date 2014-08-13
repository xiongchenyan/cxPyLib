'''
Created on Aug 13, 2014
load top n docs from input queries
in: q, cash dir
out: docno
@author: cx
'''
import site
site.addsitedir('/bos/usr4/cx/PyCode/cxPylib')
from IndriPackedRes import *

import sys

if 4 != len(sys.argv):
    print '3 para: query + cashdir + out'
    sys.exit()
    
    
CacheDir = sys.argv[2]
out = open(sys.argv[3],'w')

for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    lDoc = ReadPackedIndriRes(CacheDir + '/' + query,100)
    for Doc in lDoc:
        print >>out, '%s' %(Doc.DocNo)
out.close()



