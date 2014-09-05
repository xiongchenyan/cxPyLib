'''
Created on Sep 5, 2014
in: qid\tquery
out: qid\t #weight( 0.5 (term.title) 0.5 (term.body) )
@author: cx
'''

import sys

def FormOneQ(query):
    vCol = query.split()
    vTitle = [item + '.title' for item in vCol]
    vBody = [item + '.body' for item in vCol]
    res = '#weight( 0.5 (%s) 0.5 (%s)' %(' '.join(vTitle), ' '.join(vBody))
    return res


if 3 != len(sys.argv):
    print "query + output field query"
    sys.exit()
    
out = open(sys.argv[2],'w')

for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    print >> out,qid + '\t' + FormOneQ(query)
    
out.close()
