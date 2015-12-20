'''
Created on Dec 19, 2015 7:41:54 PM
@author: cx

what I do:
    I fetch target doc's texts
what's my input:
    ClueWeb doc (warc)
    output
what's my output:
    DocNo \t context

'''



import sys,warc
from boilerpipe.extract import Extractor

import logging
import traceback
def Process(DocIn,OutName):
    out = open(OutName,'w')
    
    In = warc.open(DocIn)
    logging.info('reading [%s]', DocIn)
    for cnt,r in enumerate(In):
        if not 'warc-trec-id' in r:
            if 0 != cnt:
                logging.warn('[%d] doc no doc no',cnt)
            continue
        DocNo = r['warc-trec-id']
        logging.debug('get [%s]', DocNo)
        res = ""
        for line in r.payload:
            res += line + ' '
        if len(res) == 0:
            continue
        try:
            extractor = Extractor(extractor='ArticleExtractor',html=res)
            text = extractor.getText()
            text.replace('\n',' ').replace('\t',' ')
            print >>out, DocNo + '\t' + text.encode('ascii','ignore')
#             print DocNo + '\t' + text.encode('ascii','ignore')
        
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(e.message)
            
        if 0 == (cnt % 100):
            logging.info('parsed [%d] doc', cnt)

    out.close()
    print 'finished'
    
if 3 != len(sys.argv):
    print 'I get doc text from warc file'
    print 'ClueWebIn+ output'
    sys.exit()
    
    
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
    
Process(sys.argv[1], sys.argv[2])                    
                    