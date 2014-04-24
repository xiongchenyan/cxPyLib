'''
Created on Apr 21, 2014
read file at key level
@author: cx
'''
import gzip

class KeyFileReaderC(object):
    def Init(self):
        self.InFile = ""
        self.UseGzip = False
        self.lKeyIndex = [0]
        self.Spliter = '\t'
        self.MaxLinePerKey = 1000000
        self.LastvCol = []
        self.InName = ""
    def __init__(self):
        self.Init()
        
        
    def open(self,InName,mode = 'r'):
        self.InName = InName
        if self.UseGzip:
            self.InFile = gzip.open(InName,mode)
        else:
            self.InFile = open(InName,mode)
            
    def empty(self):
        return "" == self.InName
            
    def close(self):
        if not self.empty():
            self.InFile.close()
            self.InName = ""
    
    
    def GenerateKey(self,vCol):
        key = ""
        for i in self.lKeyIndex:
            key += vCol[i] + self.Spliter
        return key.strip(self.Spliter)
        
        
    def ReadNextKey(self):
        lvCol = [] #one object's all triples
        if self.LastvCol != []:
            lvCol.append(self.LastvCol)
            self.LastvCol = []
        
        CurrentKey = ""    
        for line in self.InFile:
            vCol = line.strip().split(self.Spliter)
            ThisKey = self.GenerateKey(vCol)
#             print "read [%s]" %(line.encode('utf-8','ignore'))
            if [] == vCol:
                continue
            if CurrentKey == "":
                CurrentKey = ThisKey
            if ThisKey != CurrentKey:
                self.LastvCol = vCol
                break
            lvCol.append(vCol)
        return lvCol
    
    
    def __iter__(self):
        return self
    
    def next(self):
        lvCol = self.ReadNextKey()
        if lvCol == []:
            raise StopIteration
        return lvCol    
            
        
