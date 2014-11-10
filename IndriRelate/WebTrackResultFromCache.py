'''
Created on Nov 9, 2014 10:12:23 PM
@author: cx

what I do:
generate web track format ranking result from CacheDir
what's my input:
queries + cache dir
what's my output:
a rank in cache dir
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from IndriRelate.IndriInferencer import *
import sys


if 3 != len(sys.argv):
    print "query + cache dir"
    sys.exit()
    
    
for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    lDoc = ReadPackedIndriRes(sys.argv[2] + '/' + query, 1000)
    for i in range(len(lDoc)):
        print "%s Q0 %s %d %f base" %(qid,lDoc[i].DocNo,i+1,lDoc[i].score)
        


