'''
Created on Dec 19, 2015 7:52:43 PM
@author: cx

what I do:
    submit one job for each parser
what's my input:
    CW12 dir
    out dir
what's my output:
    same organization, each file is parsed

'''

import subprocess
import os
import ntpath
import json

def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName


def Process(InDir,OutDir):
    lFName = WalkDir(InDir)
    
    lFName = [fname for fname in lFName if fname.endswith('warc.gz')]
    
    
    lCmd = ['qsub','python','ParseClueWebDoc.py']
    for fname in lFName:
        OutName = OutDir + '/' + fname[len(InDir):].replace('.warc.gz','')
        MidDir = ntpath.dirname(OutName)
        if not os.path.exists(MidDir):
            os.makedirs(MidDir)
        print 'submitting %s' %(json.dumps(lCmd))
        print subprocess.check_output(lCmd + [fname,OutName])
        
        
import sys

if 3 != len(sys.argv):
    print 'parse CW'
    print 'CW InDir + outdir'
    sys.exit()
Process(sys.argv[1], sys.argv[2])
        
    
