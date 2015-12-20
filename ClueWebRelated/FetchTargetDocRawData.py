'''
Created on Dec 19, 2015 7:08:15 PM
@author: cx

what I do:
    I fetch target doc's texts
what's my input:
    ClueWeb Dir (now working for 12, 09 need specific warc parckage)
    taget doc No
        one line one docno
what's my output:
    DocNo \t raw text (everything)


'''

import sys,warc
import os

def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName


def Process(InDir,DocNoIn,OutName):
    sDocNo = set(open(DocNoIn).read().splitlines())
    out = open(OutName,'w')
    lFName  = WalkDir(InDir)
    
    for FName in lFName:
        In = warc.open(FName)
        print 'reading [%s]' %(FName)
        for r in In:
            if r['warc-trec-id'] in sDocNo:
                res = ""
                for line in r.payload:
                    res += line + ' '
                print >>out, r['warc-trec-id'] + '\t' + line.strip()

    out.close()
    print 'finished'
    
if 4 != len(sys.argv):
    print 'I get target doc raw data from warc file'
    print 'ClueWebInDir + TargetDocNo in + output'
    sys.exit()
    
    
Process(sys.argv[1], sys.argv[2], sys.argv[3])                    
                        
