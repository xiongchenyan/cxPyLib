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



def Process(DocIn,OutName):
    out = open(OutName,'w')
    
    In = warc.open(DocIn)
    print 'reading [%s]' %(DocIn)
    for cnt,r in enumerate(In):
        DocNo = r['warc-trec-id']
        res = ""
        for line in r.payload:
            res += line + ' '
        extractor = Extractor(extractor='ArticleExtractor',html=res)
        print >>out, DocNo + '\t' + extractor.getText()
        if 0 == (cnt % 1000):
            print 'parsed [%d] doc' %(cnt)

    out.close()
    print 'finished'
    
if 3 != len(sys.argv):
    print 'I get doc text from warc file'
    print 'ClueWebIn+ output'
    sys.exit()
    
    
Process(sys.argv[1], sys.argv[3])                    
                        