'''
Created on Jul 22, 2014
rename indir cached res
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriRelate.IndriPackedRes import *
import os
import sys

if 4 != len(sys.argv):
    print "3para: query in name + query to rename + cashdir"
    sys.exit()
    
    
CashDir = sys.argv[3]

hQName = {}
for line in open(sys.argv[2]):
    qid,query = line.strip().split('\t')
    hQName[qid] = query
    
for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    try:
        os.rename(CashDir + '/' + query, CashDir + '/' + hQName[qid])
    except OSError:
        print "rename [%s] to [%s] failed" %(CashDir + '/' +query, CashDir + '/' +hQName[qid])
    


