'''
Created on Dec 9, 2013
test ctf loader
@author: cx
'''
import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
import sys
from IndriRelate.CtfLoader import *
if 3 != len(sys.argv):
    print "2 para: TermCtfIn + TermIn"
    sys.exit()
    
UnitTest(sys.argv[1],sys.argv[2])
