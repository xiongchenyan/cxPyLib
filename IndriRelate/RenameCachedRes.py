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

if 5 != len(sys.argv):
    print "3para: query in name + query to rename + cashdir + name length (101|104)"
    sys.exit()
    
    
CashDir = sys.argv[3]
NameLen = int(sys.argv[4])
hQName = {}
for line in open(sys.argv[2]):
    qid,query = line.strip().split('\t')
    hQName[qid] = query
    
for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    try:
        InName = CashDir + '/' + query
        InName = InName[:NameLen]
        os.rename(InName, CashDir + '/' + hQName[qid])
    except OSError:
        print "rename [%s] to [%s] failed" %(InName, CashDir + '/' +hQName[qid])
    


