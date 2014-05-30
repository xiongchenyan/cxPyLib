'''
Created on May 30, 2014

@author: cx
'''

import sys

def FormKey(line):
    global lKey
    vCol = line.strip().split('\t')
    Key = ""
    for i in lKey:
        Key += "%s\t" %(vCol[i])
    return Key.strip('\t')

def ReadKeys(InName):
    global lKey
    hKey = {}
    for line in InName:
        hKey[FormKey(line)] = True
    return hKey
        
        


if 4 >= len(sys.argv):
    print " 3 or 4 para: input + target keys + output + keylist (i.e. 0#1#2)"
    sys.exit()
    
lKey=[0]
if len(sys.argv) > 4:
    lKey = [int(item) for item in sys.argv[4].split('#')]
    
hKey = ReadKeys(sys.argv[2])

out = open(sys.argv[3],'w')
for line in open(sys.argv[1]):
    Key = FormKey(line)
    if Key in hKey:
        print >>out, line.strip()
        
out.close()

