'''
Created on Dec 19, 2015 7:15:29 PM
@author: cx

what I do:
    I submit FetchTargetDocRawData
what's my input:
    DirPre
    TargetDocNo
    OutPre
what's my output:
    submit one job for one Dir

'''

import subprocess,sys
from FetchTargetDocRawData import *

if 4 != len(sys.argv):
    print 'I submit FetchTargetDocRawData.py (make sure same dir)'
    print 'InPre + TargetDocNo + outPre'
    sys.exit()
    
lCmd = ['qsub','python','FetchTargetDocRawData.py']
for i in range(20):
    InName = sys.argv[1] + '%02d' %(i)
    OutName = sys.argv[3] + '%02d' %(i)
    lThisCmd = lCmd + [InName,sys.argv[2],OutName]
    print subprocess.check_output(lThisCmd)
    

    
