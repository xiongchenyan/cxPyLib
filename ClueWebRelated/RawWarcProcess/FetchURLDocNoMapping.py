'''
Created on Sep 9, 2015 5:42:51 PM
@author: cx

what I do:
    I fetch url to doc no mapping
what's my input:
    a CW09 dir to work on
what's my output:
    URL->DocNo mapping of all warc files in the dir

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import warc,sys
from cxBase.WalkDirectory import WalkDir

def FetchOneDirURL(InDir,OutName):
    lFName = WalkDir(InDir)
    out = open(OutName,'w')
    for InName in lFName:
        In = warc.open(InName)
        while True:
            try:
                record = In.read_record()
            except (AssertionError, EOFError) as e:
                break
            if ('warc-trec-id' in record) & ('warc-target-uri' in record):
                print >> out, record['warc-target-uri'] + '\t' + record['warc-trec-id']
                
        print '[%s] finished' %(InName)
    out.close()
    print 'dir [%s] finished' %(InDir)
    return True


if 3 != len(sys.argv):
    print 'I will write all url-docno pairs'
    print 'cw09 dir + out'
    sys.exit()
    
FetchOneDirURL(sys.argv[1],sys.argv[2])

