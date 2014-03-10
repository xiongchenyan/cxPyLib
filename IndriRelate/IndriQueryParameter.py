'''
Created on Nov 4, 2013
make Indri run query parameters for a given set of queries
@author: cx
'''


import copy

class IndriQueryParaC:
    lParaField=[]
    llQueryField=[]
    lQueryPara=[]
    
    def __init__(self):
        self.lParaField = []
        self.llQueryField = []
        self.lQueryPara = []
        
    def SetField(self,FieldName,FieldValue):
        self.lParaField.append([FieldName,FieldValue])
        return True
    
    def SetQueryPara(self,QParaName,QParaValue):
        self.lQueryPara.append([QParaName,QParaValue])
        return True
    
    def AddQuery(self,Query,QueryId):
        lQ = copy.deepcopy(self.lQueryPara)
#         lQ.append([Query,QueryId])
        lQ.append(['text',Query])
        lQ.append(['number',QueryId])
        self.llQueryField.append(lQ)
        
    def Out(self):
        res = "<parameters>\n"
        for para in self.lParaField:
            res += '<' + para[0] + '>' + para[1] + "</" + para[0] + ">\n"
        for lQ in self.llQueryField:
            res += '<query>\n'
            for qpara in lQ:
                res += '<' + qpara[0] + '>' + qpara[1] + '</' + qpara[0] + '>\n'
            res += '</query>\n'
        res += "</parameters>"
        return res
    
    def GetNumOfQ(self):
        return len(self.llQueryField)
    
    def CopyPara(self, QueryPara):
        self.lParaField = copy.deepcopy(QueryPara.lParaField)
        self.lQueryPara = copy.deepcopy(QueryPara.lQueryPara)
        return True
    
    def Dump(self,FName):
        out= open(FName,'w')
        print >> out,"<parameters>"
        for para in self.lParaField:
            print >> out, '<' + para[0] + '>' + para[1] + "</" + para[0] + ">"
        for lQ in self.llQueryField:
            print >> out, '<query>'
            for qpara in lQ:
                print >> out, '<' + qpara[0] + '>' + qpara[1] + '</' + qpara[0] + '>'
            print >> out, '</query>'
        print >>out,"</parameters>"
        out.close();
        return True
    
    

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


        
    

