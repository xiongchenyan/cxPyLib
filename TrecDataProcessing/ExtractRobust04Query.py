'''
Created on Aug 5, 2014

@author: cx
'''

import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.TextBase import *

if 3 != len(sys.argv):
    print "q in + out"
    sys.exit()
    
out = open(sys.argv[2],'w')
qid = '0'
flag = False
for line in open(sys.argv[1]):
    line = line.strip()
    if '<num>' in line:
        qid = line.replace('<num> Number:','').strip()
    if '<title>' in line:
        query = line.replace('<title>','').strip().lower()
        if query == '':
            flag = True
            continue
        else:
            print >>out, qid + '\t' + TextBaseC.DiscardNonAlphaNonDigit(query)
    if flag:
        print >>out, qid + "\t" +  TextBaseC.DiscardNonAlphaNonDigit(line.strip())
        flag = False
out.close()
    