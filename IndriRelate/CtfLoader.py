'''
Created on Dec 5, 2013
load ctf from a file
file is made by c++ calling IndriAPI in query enviroment
will load and keep in class, output as service
@author: cx
'''


class TermCtfC:
    
    def __init__(self,InName = ""):
        self.Init()
        if "" != InName:
            self.Load(InName)
            
    def Init(self):
        self.TotalCnt = 0
        self.hTermCtf = {}
        return True    
    def Load(self,InName):
        '''
        first line is always total cnt
        '''
        cnt = 0
        for line in open(InName):            
            vCol = line.strip().split()
            if cnt == 0:
                cnt += 1
#                 print vCol[0]
                self.TotalCnt = int(vCol[0])
                continue
            term = vCol[0]
            value = float(vCol[1])
            self.hTermCtf[term] = value
        return True    
    def GetCtf(self,term):
        if not term in self.hTermCtf:
            return 0
        return self.hTermCtf[term]
    
    def GetCtfProb(self,term):
        return self.GetCtf(term) / float(self.TotalCnt)
    


def UnitTest(TermCtrIn,TestTermIn):
    TermCtfCenter = TermCtfC(TermCtrIn)
    for line in open(TestTermIn):
        term = line.strip()
        print term + "\t%f" %(TermCtfCenter.GetCtf(term))
    return True