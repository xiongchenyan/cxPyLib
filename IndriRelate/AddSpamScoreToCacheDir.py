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

import sys

from IndriPackedRes import *
from cxBase.WalkDirectory import WalkDir
if 3 > len(sys.argv):
    print "cachedir + spamscore files"
    sys.exit()
    
    
print "loading spam score"
hDocSpam = {}

for fname in sys.argv[2:]:
    for line in open(fname):
        score,DocNo = line.strip().split()
        hDocSpam[DocNo] = score
        
    print fname + " readed"
    
out = open(sys.argv[1]+"_WaterlooSpamScore",'w')
for fname in WalkDir(sys.argv[1]):
    lDoc = ReadPackedIndriRes(fname,  1000)
    for doc in lDoc:
        if not doc.DocNo in hDocSpam:
            continue
        print >>out, doc.DocNo + "\t" + hDocSpam[doc.DocNo]
    print "%s done" %(fname)
out.close()
print "finished"
    

