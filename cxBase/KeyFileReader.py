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
        self.KeyIndex = 0
        self.Spliter = '\t'
        self.MaxLinePerKey = 100000
        self.LastvCol = []
    def __init__(self):
        self.Init()
        
        
    def open(self,InName,mode = 'r'):
        if self.UseGzip:
            self.InFile = gzip.open(InName,mode)
        else:
            self.InFile = open(InName,mode)
            
            
    def close(self):
        self.InFile.close()
        
        
    def ReadNextKey(self):
        lvCol = [] #one object's all triples
        if self.CurrentvCol != []:
            lvCol.append(self.CurrentvCol)
            self.CurrentvCol = []
        
        CurrentKey = ""    
        for line in self.In:
            vCol = line.strip().split(self.Spliter)
            if [] == vCol:
                continue
            if CurrentKey == "":
                CurrentKey = vCol[self.KeyIndex]
            if vCol[self.KeyIndex] != CurrentKey:
                self.CurrentvCol = vCol
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
            
        
