'''
Created on Mar 11, 2014
unit test
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
import sys

from AdhocEva import *
from cxBase.base import cxConf


if 2 != len(sys.argv):
    print "1 para conf:\nin\nqrel\nevadepth\nout"
    sys.exit()
    
AdhocEvaUnitTest(sys.argv[1])
print "done"