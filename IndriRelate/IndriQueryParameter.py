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
    
    


        
    

