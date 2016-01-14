'''
Created on Jan 13, 2016 10:36:54 PM
@author: cx

what I do:

what's my input:

what's my output:


'''

import sys,string


if 3 != len(sys.argv):
    print 'in + out (encode to ascii)'
    sys.exit()

out = open(sys.argv[2],'w')
ErrCnt  = 0
for cnt, text in enumerate(open(sys.argv[1])):
    try:
        text = text.strip().encode('ascii','ignore')
        text = filter(lambda x: x in string.printable, text)
        print >>out, text
    except Exception as e:
        print Exception
        ErrCnt += 1
        
        
print 'finished [%d/%d]' %(ErrCnt,cnt)
        
        
