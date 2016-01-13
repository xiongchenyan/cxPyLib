'''
Created on Dec 19, 2015 7:41:54 PM
@author: cx

what I do:
    I fetch target doc's contents using boiler pipe
    1: discard HTML header (those before <html)
    2: boilerpipe for content
    3: tokenization, discard non English and not number terms
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
import string
import nltk

def DiscardHTMLHeader(RawHtml):
    p = RawHtml.find('<html')
    if p == -1:
        return ""
    res = RawHtml[p:]
    return res

def TextClean(text):
    res = text
    res = filter(lambda x: x in string.printable, res)
    
    lToken = nltk.word_tokenize(res)
    for i in range(len(lToken)):
        token = filter(lambda x: x.isalnum(), lToken[i])
        lToken[i] = token.lower()
    res = ' '.join(lToken)
    res = ' '.join(res.split())
    return res

def Process(DocIn,OutName):
    out = open(OutName,'w')
    
    logging.info('reading [%s]', DocIn)
    ErrCnt = 0
    for cnt,line in enumerate(open(DocIn)):
        vCol = line.strip().split('\t')
        DocNo = vCol[0]
        RawHtml = ' '.join(vCol[1:])
        RawHtml = DiscardHTMLHeader(RawHtml)
        if "" == RawHtml:
            ErrCnt += 1
            continue
        try:
            extractor = Extractor(extractor='ArticleExtractor',html=RawHtml)
            text = extractor.getText()
            text = text.replace('\n',' ').replace('\t',' ')
            text = text.encode('ascii','ignore')
            text = TextClean(text)
            if "" != text:
                print >>out, DocNo + '\t' + text
#             print DocNo + '\t' + text.encode('ascii','ignore')
        
        except Exception as e:
            ErrCnt += 1
            
        if 0 == (cnt % 100):
            logging.info('parsed [%d] doc [%d] Err', cnt,ErrCnt)

    out.close()
    logging.info('finished [%d] doc [%d] Err', cnt,ErrCnt)
    
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
                    