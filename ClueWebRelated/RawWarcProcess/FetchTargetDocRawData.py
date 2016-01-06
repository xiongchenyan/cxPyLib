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
import ntpath
from boilerpipe.extract import Extractor
import logging
import traceback


def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName


def Process(InDir,DocNoIn,OutName):
    sDocNo = set(open(DocNoIn).read().splitlines())
    sDocPre = set(['-'.join(DocNo.split('-')[1:3]) for DocNo in sDocNo])
    out = open(OutName,'w')
    lFName  = WalkDir(InDir)
    
    for FName in lFName:
        if ntpath.basename(FName).replace('.warc.gz','') in sDocPre:
            logging.info('target file [%s]',FName)
            In = warc.open(FName)
            logging.info('reading [%s]', FName)
            cnt = 0
            try:
                for r in In:
                    if not 'warc-trec-id' in r:
                        continue
                    cnt += 1
                    DocNo = r['warc-trec-id']
                    if DocNo in sDocNo:
                        logging.info('get doc [%s]',DocNo)
                        res = ""
                        for line in r.payload:
                            res += line + ' '
                        try:
                            extractor = Extractor(extractor='ArticleExtractor',html=res)
                            text = extractor.getText()
                            text.replace('\n',' ').replace('\t',' ')
                            print >>out, DocNo + '\t' + text.encode('ascii','ignore')
                #             print DocNo + '\t' + text.encode('ascii','ignore')
                        
                        except Exception as e:
                            logging.error(traceback.format_exc())
                            logging.error(e.message)
            except AssertionError:
                logging.error('[%s] asserction err at [%d] file',FName,cnt)

    out.close()
    print 'finished'
    
if 4 != len(sys.argv):
    print 'I get target doc raw data from warc file'
    print 'ClueWebInDir + TargetDocNo in + output'
    sys.exit()
    
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
    
Process(sys.argv[1], sys.argv[2], sys.argv[3])                    
                        
