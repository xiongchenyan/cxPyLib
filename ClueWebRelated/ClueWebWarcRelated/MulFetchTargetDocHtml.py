'''
Created on Jan 11, 2016 5:10:40 PM
@author: cx

what I do:
    I sub jobs to fetch target doc's html using java jar
    for each input warc file,
        check if it can contain target DocNo
            if so, submit a job
                java -jar ./FetchTargetDocHtml.jar warc outname TargetDocNo 
what's my input:
    Clueweb dir
    Target DocNo
    outdir
what's my output:
    target doc nos in the outdir

'''

import subprocess
import ConfigParser
import json,sys,os


import site
import ntpath
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.WalkDirectory import WalkDir




def LoadTargetDocNoAndFormTargetFilePre(TargetDocNoIn):
    lDocNo = open(TargetDocNoIn).read().splitlines()
    sDocNo = set(lDocNo)
    
    lFilePre = ['-'.join(DocNo.split('-')[1:3]) for DocNo in lDocNo]
    sFilePre = set(lFilePre)
    
    return sDocNo,sFilePre



def SubmitJavaJobs(InDir,OutDir,TargetDocNoIn):
    '''
    submit jobs for all file in InDir if it has target doc
    '''
    sDocNo,sFilePre = LoadTargetDocNoAndFormTargetFilePre(TargetDocNoIn)
    
    lFName = WalkDir(InDir)
    
    lBaseCmd = ['qsub','java','-jar','./FetchTargetDocHtml.jar']
    cnt = 0
    for fname in lFName:
        key = ntpath.basename(fname).split('.')[0]
        if not key in sFilePre:
            continue
        OutName = OutDir + ntpath.basename(fname)
        lCmd = lBaseCmd + [fname,OutName,TargetDocNoIn]
        print 'submitting %s' %(json.dumps(lCmd))
        print subprocess.check_output(lCmd)
        cnt += 0
        
    print '[%d] job submited' %(cnt)
    return


import sys

if 4 != len(sys.argv):
    print 'I submit java jobs (FetchTargetDocHtml.jar) to get html for target doc'
    print ' 3 para: ClueWeb warc InDir + OutDir + TargetDocNo'
    sys.exit()
    
SubmitJavaJobs(sys.argv[1], sys.argv[2], sys.argv[3])
    
    
