'''
Created on Jan 6, 2016 3:29:08 PM
@author: cx

what I do:
    I filter qrel file to only keep cat b ones
what's my input:
    qrel
what's my output:
    qrel but only cat b ones are kept

'''

import sys

if 3 != len(sys.argv):
    print 'I filter qrel to cat b only'
    print 'in qrel + out'
    sys.exit()

lCatBMid = []
for i in range(12):
    lCatBMid.append('en%04d'%(i))
    
for i in range(4):
    lCatBMid.append('enwp%02d'%(i))
    
    
out = open(sys.argv[2],'w')
sCatBMid = set(lCatBMid)
for line in open(sys.argv[1]):
    line = line.strip()
    mid = line.split('-')[1]
    if mid in sCatBMid:
        print >>out, line
        
        
out.close()
print 'finished'
    
    


