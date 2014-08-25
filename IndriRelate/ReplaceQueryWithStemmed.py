'''
Created on Aug 25, 2014
in: query file + query stem
out: default q is at col[1], will replace it
@author: cx
'''

import sys

if 4 != (len(sys.argv)):
    print "3 para: to replace file + stemmed q + out"
    sys.exit()
    
hQ = {}
for line in open(sys.argv[2]):
    qid,query = line.strip().split('\t')
    hQ[qid] = query

out = open(sys.argv[3],'w')
for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    if vCol[0] in hQ:
        vCol[1] = hQ[vCol[0]]
    print >>out, '\t'.join(vCol)
out.close()
