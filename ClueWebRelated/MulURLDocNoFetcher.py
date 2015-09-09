'''
Created on Sep 9, 2015 5:49:15 PM
@author: cx

what I do:
    I submit jobs for each dir of CW09 to get url-doc no pairs
what's my input:
    cw09 dir
what's my output:
    a dir of url-doc no mappings
    done by qsub FetchURLDocNoMapping for each sub dir in input

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

import subprocess
import sys
import ntpath

if 3 != len(sys.argv):
    print 'list of CW09 dir + out dir'
    sys.exit()
    
    
lCmd = ['qsub','FetchURLDocNoMapping.py']


lFName = open(sys.argv[1]).read().splitlines()

lOutName = [sys.argv[2] + '/' + ntpath.basename(fname.strip('/')) + '_URLDocNo' for fname in lFName]

for InDir,OutName in zip(lFName,lOutName):
    ThisCmd = lCmd + [InDir,OutName]
    print '\t'.join(ThisCmd)
    print subprocess.check_output(ThisCmd)
    
    