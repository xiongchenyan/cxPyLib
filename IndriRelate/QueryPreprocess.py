'''
Created on Dec 5, 2013
do processing for query
for raw query:
    discard all none English character 
@author: cx
'''

import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
from cxBase.base import DiscardNonAlpha

def DiscardNonEnChar(query):
    return DiscardNonAlpha(query)

