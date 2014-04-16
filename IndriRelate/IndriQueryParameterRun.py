'''
Created on Apr 16, 2014

@author: cx
'''


from IndriQueryParameter import *
import sys
MaxQPerPara = 200
if 4 != len(sys.argv):
    print '3 para: fields + query + output'
    sys.exit()
    
IndriQPara = IndriQueryParaC()

for line in open(sys.argv[1]):
    line = line.strip()
    vCol = line.split('\t')
    if (len(vCol) != 2):
        print "2 col in fields: para field, name"
        sys.exit()
    IndriQPara.SetField(vCol[0], vCol[1])
    
IndriQPara.SetQueryPara('type','indri')

OutName = sys.argv[3]
OutFileCnt = 0
qid = 1
for line in open(sys.argv[2]):
    line = line.strip()
    vCol = line.split('\t')
    if (len(vCol) != 2):        
        IndriQPara.AddQuery(vCol[0],str(qid))
        qid += 1
    else:
        IndriQPara.AddQuery(vCol[0],vCol[1])
    if IndriQPara.GetNumOfQ() > MaxQPerPara:
        IndriQPara.Dump(OutName + str(OutFileCnt))
        OutFileCnt += 1
        MidQPara = IndriQueryParaC()
        MidQPara.CopyPara(IndriQPara)
        IndriQPara = IndriQueryParaC()
        IndriQPara = MidQPara

if IndriQPara.GetNumOfQ() > 0:    
    IndriQPara.Dump(sys.argv[3] + str(OutFileCnt))
