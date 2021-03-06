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
from IndriSearch.IndriDocBase import *
from IndriSearch.IndriSearchCenter import *
import sys


if 4 > len(sys.argv):
    print "query + cache dir + out"
    sys.exit()
    
CacheVersion = 'old'
out = open(sys.argv[3],'w')
if len(sys.argv) > 4:
    CacheVersion = sys.argv[4]
    IndriSearcher = IndriSearchCenterC()
    IndriSearcher.CacheDir = sys.argv[2]    

for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    if CacheVersion == 'old':
        lDoc = ReadPackedIndriRes(sys.argv[2] + '/' + query, 1000)
    else:
        lDoc = IndriSearcher.RunQuery(query)
    for i in range(len(lDoc)):
        print >>out, "%s Q0 %s %d %f base" %(qid,lDoc[i].DocNo,i+1,lDoc[i].score)

out.close()
        


