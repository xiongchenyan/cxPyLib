'''
Created on Jan 5, 2014
sample terms from a big text
in a dir + need numebr of term perfile
out to a dir
same file name, but keep term number sampled
@author: cx
'''

import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
site.addsitedir('/bos/usr4/cx/Dropbox/workspace/python/SearchResultDiversification')
from cxBase.WalkDirectory import * 

import sys
import random

if 4 != len(sys.argv):
    print "3 para: input dir + out dir + number of term perfile"
    sys.exit()
    
    


def SampleOneFile(InName,OutName,NumberOfTerm):
    lTerm = []
    for line in open(InName):
        vCol = line.strip().split()
        lTerm.extend(vCol)
    out = open(OutName,"w")
    if len(lTerm) == 0:
        out.close()
        return True    
    lRes = random.sample(lTerm,NumberOfTerm)
    print >>out, " ".join(lRes)
    out.close()
    return True

def MakeOutName(InName,OutDir):
    vCol = InName.split("/")
    return OutDir + "/" + vCol[len(vCol) - 1]


lFName = WalkDir(sys.argv[1])
NumberOfTerm = int(sys.argv[3])
for fname in lFName:
    outname = MakeOutName(fname,sys.argv[2])
    SampleOneFile(fname,outname,NumberOfTerm)
    print fname + " finished"
    
print "finished"

