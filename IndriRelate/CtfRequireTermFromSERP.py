'''
Created on Mar 10, 2014
extract target terms from SERP
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')


from IndriRelate.IndriPackedRes import *
from cxBase.base import cxConf
import sys
'''
input query, read cash res (SERP) seg all terms, uniq and output
'''

def GetTermFromSERP(lDoc):
    hTerm = {}
    for doc in lDoc:
        content = doc.GetContent()
        lTerm = content.split()
        for term in lTerm:
            if '[OOV]' == term:
                continue
            if not term in hTerm:
                hTerm[term] = 1
    return hTerm


if 2 != len(sys.argv):
    print "1para:conf file\nin\nout\ncashdir\nnumofdoc"
    sys.exit()
    
conf = cxConf(sys.argv[1])
InName = conf.GetConf("in")
OutName= conf.GetConf("out")
CashDir = conf.GetConf("cashdir")
NumOfDoc = conf.GetConf("numofdoc")

out = open(OutName,'w')
hAllTerm = {}
for line in open(InName):
    qid,query = line.strip().split('\t')
    lDoc = ReadPackedIndriRes(CashDir + "/" + query)
    hTerm = GetTermFromSERP(lDoc)
    hAllTerm = dict(hAllTerm.items() + hTerm.items())
    
for item in hAllTerm:
    print >>out,item
    
out.close()




