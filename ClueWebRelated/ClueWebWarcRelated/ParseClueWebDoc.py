'''
Created on Dec 19, 2015 7:41:54 PM
@author: cx

what I do:
    I fetch target doc's texts
what's my input:
    ClueWeb doc html
        docno \t html
what's my output:
    DocNo \t content

'''



import sys
from boilerpipe.extract import Extractor

import logging
import traceback
def Process(DocIn,OutName):
    out = open(OutName,'w')
    
    logging.info('reading [%s]', DocIn)
    for cnt,line in enumerate(open(DocIn)):
        vCol = line.strip().split('\t')
        DocNo = vCol[0]
        RawHtml = ' '.join(vCol[1:])
        try:
            extractor = Extractor(extractor='ArticleExtractor',html=RawHtml)
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
                    