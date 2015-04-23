'''
Created on Apr 22, 2015 9:07:45 PM
@author: cx

what I do:
filter raw warc file with blacklist
what's my input:
clueweb's data dir + spam blacklist
what's my output:
a new data dir, with spam filtered docs

'''

import sys,warc
import os

def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName
        

def FilterOneFile(InName,OutName,hBlack):
    In = warc.open(InName)
    Out = warc.open(OutName,'w')
    cnt = 0
    FilterCnt = 0
    while True:
        try:
            record = In.read_record()
        except (AssertionError, EOFError) as e:
            break
        cnt += 1
        if 'warc-trec-id' in record:
            if record['warc-trec-id'] in hBlack:
                FilterCnt +=  1
                continue
        Out.write_record(record)
    print '[%s] [%d/%d] filtered' %(InName,FilterCnt,cnt)
    return True


def process(InDir,OutDir,BlackInName):
    hBlack = set(open(BlackInName).read().splitlines())
    lInName = WalkDir(InDir)
    for InName in lInName:
        if not InDir in InName:
            print "InDir must be absolute path [%s]" %(InDir)
            break
        OutName = InName.replace(InDir,OutDir)
        OutPath = '/'.join(OutName.split('/')[:-1])
        if not os.path.exists(OutPath):
            os.makedirs(OutPath)
        FilterOneFile(InName, OutName, hBlack)
    return


if 4 != len(sys.argv):
    print 'indir + out dir + blackfile list'
    sys.exit()
    
process(sys.argv[1],sys.argv[2],sys.argv[3])
print "all finished"
        
            
    