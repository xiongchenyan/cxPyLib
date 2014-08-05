'''
Created on Aug 5, 2014

@author: cx
'''

import sys


if 3 != len(sys.argv):
    print "q in + out"
    sys.exit()
    
out = open(sys.argv[2],'w')
qid = '0'
for line in open(sys.argv[1]):
    line = line.strip()
    if '<num>' in line:
        qid = line.replace('<num> Number:','').strip()
    if '<title>' in line:
        query = line.replace('<title>','').strip().lower()
        print >>out, qid + '\t' + query
out.close()
    