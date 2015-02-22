'''
Created on Feb 12, 2015 11:45:07 AM
@author: cx

what I do:
I read files with separator lines
what's my input:

what's my output:


'''

import gzip

class SeparatorlineFileReaderC(object):
    def Init(self):
        self.InFile = ""
        self.UseGzip = False
        self.Spliter = '\t'
        self.MaxLinePerFile = 100000
        self.LastvCol = []
        self.InName = ""
        self.SeparatorPre = ''
        self.CurrentSeparatorLine = ""
        self.KeepSepLine = False
    def __init__(self,SeparatorPre = 'trec',KeepSepLine = False):
        self.Init()
        self.SeparatorPre = SeparatorPre
        self.KeepSepLine = KeepSepLine
        
        
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
    
    
    def IsSeparatorLine(self,line):
        if self.SeparatorPre == line[:len(self.SeparatorPre)]:
            return True
        return False    
        
    def ReadNextFile(self):
        '''
        start from a separator line, or not,
        read until next separator line
        '''
        
        lvCol = [] #one object's all cols
        cnt = 0
        for line in self.InFile:
            line = line.strip()
            if "" == line:
                continue
            if self.IsSeparatorLine(line):
                self.CurrentSeparatorLine = line
                if [] != lvCol:
                    break
                else:
                    continue
            if self.KeepSepLine:
                vCol = [self.CurrentSeparatorLine] + line.split(self.Spliter)
            else:
                vCol = line.split(self.Spliter)
            vCol = [col.strip() for col in vCol]
            if [] == vCol:
                continue
            if cnt < self.MaxLinePerFile:
                lvCol.append(vCol)
            cnt += 1
        return lvCol
    
    
    def __iter__(self):
        return self
    
    def next(self):
        lvCol = self.ReadNextFile()
        if lvCol == []:
            raise StopIteration
        return lvCol    
