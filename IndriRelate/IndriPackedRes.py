'''
Created on Oct 2, 2013
10.2/2013: basic read from doc vector set. input format is the QueryIndriC (C++ code)'s output.
TBD: add support to raw doc string. as FACC1 data will require the full doc string.
@author: cx
'''

'''
May 19 2014.
Put the read function to PackedIndriResC class.
not tested
'''


class FieldC:
    begin = 0
    end = 0
    name = ""
    def __init__(self,line = ""):
        self.begin = 0
        self.end = 0
        self.name = ""
        if (line != ""):
            vCol = line.split(" ")
            self.name = vCol[0]
            self.begin = int(vCol[1])
            self.end = int(vCol[2])
    def out(self):
        return self.name + " " + str(self.begin) + " " + str(self.end) 
    

#raw doc content not implemented. all information now comes from DocVector
class PackedIndriResC(object):
    DocNo = ""
    score = 0
    lPosition = []
    lTerm = []
    lField = []
    
    content = ""
    title=""
    hField = {}
    RawContent = "";
    
    def Init(self):
        self.DocNo = ""
        self.score = 0
        self.lPosition = []
        self.lTerm = []
        self.lField = []
        self.hField={}
        self.RawContent = ""    
    def __init__(self,lLine = []):
        self.Init()
        if [] != lLine:
            self.Loads(lLine)
            

    def dumps(self):
        return self.out()
    
    def ContainTerm(self,term):
        return term in self.lTerm
    
        
    def SetHField(self):
        for i in range(0,len(self.lField)):
            if not self.lField[i].name in self.hField:
                self.hField[self.lField[i].name] = []
            self.hField[self.lField[i].name].append(i)  
        return True    
    
    #return a string of target fields.
    def GetField(self,FieldName):
        res = []
        if (self.lField != []) &(self.hField == {}):
            self.SetHField()
        if not FieldName in self.hField:
            return "\t".join(res)
        lP = self.hField[FieldName]
#        print "FieldName[%s] position l [%s]" %(FieldName,str(lP))        
        for p in lP:
#            print "p[%d] len [%d]" %(p,len(self.lField))
            begin = self.lField[p].begin
            end = self.lField[p].end
            for i in range(begin,end):
                res.append(self.lTerm[self.lPosition[i]])
        return "\t".join(res)
    
    def GetTitle(self):
        if (self.title == ""):
            self.title = self.GetField('title')
        return self.title
    def GetContent(self):
        if (self.content == ""):
            for p in self.lPosition:
                self.content += self.lTerm[p] + " "
            self.content = self.content.strip(" ").lower()
        return self.content
    
    def GetSnippet(self,query):
        #fetch the snippet of query
        #the first appearance of query
        #query must be pre processed (stemmed)        
        content = self.GetContent()
        position = content.find(query.lower())
        if -1 == position:
            return ""
        st = max(0,position - 100)
        ed = min(len(content),position + 100)
        snippet = content[st:ed]
        lTerm = snippet.split()
        if len(lTerm) < 2:
            return ""
        return " ".join(lTerm[1:len(lTerm) - 1])
        
    def GetLen(self):
        return len(self.lPosition)
    
    
    def Loads(self,lLine):
        cnt = 0
        bToReadDocRaw = False
        for line in lLine:
            line = line.strip('\n').strip('\t')
#             print "working on line [%s] with cnt [%d]" %(line,cnt)
            if 'EOD' == line.strip():
                cnt = 0
                continue
            vCol = line.split('\t')
            if 0 == cnt:
    #             print json.dumps(vCol)            
                self.DocNo = vCol[0]            
                self.score = float(vCol[1])
                if (len(vCol) > 2):
                    if vCol[2] == '1':
                        bToReadDocRaw = True                  
            if 1 == cnt:
                if bToReadDocRaw:
                    if line == "<DOCRAW>":
                        continue
                    if line == "</DOCRAW>":
                        bToReadDocRaw = False #read finished
                        continue
                    self.RawContent += line + "\n"
                    continue                      
                self.lTerm = list(vCol)
            if 2 == cnt:
                for col in vCol:                    
                    try:
                        self.lPosition.append(int(col))
                    except ValueError:
                        print "[%s] not int" %(self.DocNo,line,col)
            if 3 == cnt:
                for col in vCol:
                    field = FieldC(col)
                    self.lField.append(field)              
                self.SetHField()
            if 4 == cnt:
                cnt  = -1
            cnt += 1
#             print "cnt add to [%d]" %(cnt)
        return True
    
    def out(self):
        res = ""
        res += self.DocNo + "\t" + str(self.score)
        if self.RawContent == "":
            res += '\t0\n'
        else:
            res += '\t1\n'
            res += '<DOCRAW>\n' + self.RawContent + "\n</DOCRAW>\n"            
        res += "\t".join(self.lTerm) + "\n"
        for p in self.lPosition:
            res += str(p) + "\t"
        res = res.strip('\t')
        res += "\n"
        if len(self.lField) != 0:
            for field in self.lField:
                res += field.out() + "\t"
            res = res.strip("\t")
            res += '\n'        
        res += 'EOD'
        return res
    
import json    
#read packed indri res from InName.
#there are multiple docs in one file, MaxRes sets how many i want
#return a list of PackedIndriResC
def ReadPackedIndriRes(InName,MaxRes=50):
    lPackedIndriRes = []
    cnt = 0    
    bToReadDocRaw = False
    lLine = []
    for line in open(InName):
        line = line.strip('\n')
        vCol = line.split('\t')
        if 0 == cnt:
            lLine = []
            if (len(lPackedIndriRes) >= MaxRes):
                break
#             print json.dumps(vCol)            
            if (len(vCol) > 2):
                if vCol[2] == '1':
                    bToReadDocRaw = True
        if 1 == cnt:
            if bToReadDocRaw:
                if line == "<DOCRAW>":
                    lLine.append(line)
                    continue
                if line == "</DOCRAW>":
                    bToReadDocRaw = False #read finished
                    lLine.append(line)
                    continue
                lLine.append(line)
                continue
        lLine.append(line)
        if (4 == cnt) | ('EOD' == line.strip()):            
            cnt  = -1
            Doc = PackedIndriResC(lLine)
            lPackedIndriRes.append(Doc)
        cnt += 1
    return lPackedIndriRes


def SegDocNoFromDocs(lDoc):
    lDocNo = []
    for doc in lDoc:
        lDocNo.append(doc.DocNo)
    return lDocNo