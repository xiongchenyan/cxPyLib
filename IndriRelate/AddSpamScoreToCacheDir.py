'''
Created on Nov 6, 2014 1:50:21 PM
@author: cx

what I do:
I add spam score of DocNo's in the target dir
what's my input:
CacheDir + spam score files
what's my output:
CacheDir_WaterlooSpamScore:
    DocNo\tSpamScore
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import sys

from IndriPackedRes import *
from cxBase.WalkDirectory import WalkDir
if 3 > len(sys.argv):
    print "cachedir + spamscore files"
    sys.exit()
    


hInCacheDocNo = {}

for fname in WalkDir(sys.argv[1]):
    lDoc = ReadPackedIndriRes(fname,  1000)
    for doc in lDoc:
        hInCacheDocNo[doc.DocNo] = 0
    print "%s done" %(fname)

    

out = open(sys.argv[1]+"WaterlooSpamScore",'w')
    
print "loading spam score"

for fname in sys.argv[2:]:
    for line in open(fname):
        score,DocNo = line.strip().split()
        if DocNo in hInCacheDocNo:
            print >> out, DocNo + '\t' + score        
    print fname + " readed"

out.close()
print "finished"