'''
Created on Mar 20, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import *
import sys

conf = cxConf(sys.argv[1])

print conf.GetConf('in')
