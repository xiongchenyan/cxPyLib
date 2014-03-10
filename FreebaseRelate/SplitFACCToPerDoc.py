'''
Created on Jan 7, 2014
now FACC per file is too big
split them to one doc facc per file.
    doc file name made by function
input: FACC dir + list of query + SERP folder
output: out to a dir, create sub dirs, and put doc in them. only work on doc in SERP
@author: cx
'''



import sys
import site
import os
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
site.addsitedir('/bos/usr4/cx/Dropbox/workspace/python/SearchResultDiversification')

from cxBase.base import *
from cxBase.WalkDirectory import *
from IndriRelate.IndriPackedRes import *


def LoadAllDoc(QInName,CashDir):
    hDoc = {}
    for line in open(QInName):
        InName = CashDir + "/" + line.strip()
        lDoc = ReadPackedIndriRes(InName)
        for doc in lDoc:
            hDoc[doc.DocNo] = True
    return hDoc


def MakeFName(InitDir,DocNo):
    vCol = DocNo.split('-')
    FName = InitDir + "/" + vCol[1] + "/" + vCol[2] + "/" + DocNo
    return FName


def ProcessOneFile(InName,OutDir,hDoc):
    NowDoc = ""
    lLine = []
    for line in open(InName):
        line = line.strip()
        vCol = line.split('\t')
        DocNo = vCol[0]
        if not DocNo in hDoc:
            continue
        if NowDoc == "":
            NowDoc = DocNo
        if DocNo != NowDoc:
            OutOneDocNo(OutDir,NowDoc,lLine)
            lLine = []
            NowDoc = DocNo
        lLine.append(line)
    return True
            
            

def OutOneDocNo(OutDir,DocNo,lLine):
    FName = MakeFName(OutDir,DocNo)
    Dir = os.path.dirname(FName)
    if not os.path.exists(Dir):
        os.makedirs(Dir)
    out = open(FName,'w')
    print >> out,"\n".join(lLine)
    out.close()
    return True
    
    
if 5 != len(sys.argv):
    print "4 para: query in + cashdir + facc dir + outdir"
    sys.exit()
    
hDoc = LoadAllDoc(sys.argv[1],sys.argv[2])
lInName = WalkDir(sys.argv[3])
for InName in lInName:
    print "on [%s]" %(InName)
    ProcessOneFile(InName,sys.argv[4],hDoc)
    
print "finished"






    