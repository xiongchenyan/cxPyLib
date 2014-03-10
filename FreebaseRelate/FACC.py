'''
Created on Jan 2, 2014
read a load FACC data
grouped as docno
@author: cx
'''
import copy

class FaccObjC:
    
    
    def Init(self):
        self.Mid = ""
        self.st = 0
        self.ed = 0
        self.Prob = 0
        self.GeneralProb = 0
        self.entity = ""
        return
    
    def __init__(self,line = ""):
        self.Init()
        if "" != line:
            self.Set(line)
        return
    
    def Set(self,line):
        vCol = line.split('\t')
        self.entity = vCol[2]
        self.st = int(vCol[3])
        self.ed = int(vCol[4])
        self.Prob = float(vCol[5])
        self.GeneralProb = float(vCol[6])
        lMid = vCol[7].split('/')       
        self.Mid = lMid[len(lMid) - 1]
        return True

class FACCForDoc:    
    
    def Init(self):
        self.DataDir = ""
        self.DocNo = ""
        self.lObj = []
        self.hObj = {}
        self.FaccLen = 0
        return
    
    def __init__(self):
        self.Init()
        
    def SetDataDir(self,TargetDir):
        self.DataDir = TargetDir
    
    def LoadFromSplit(self,DocNo):
        self.DocNo = DocNo
        FName = self.MakeFileNameForSplit(DocNo)
        try:
            for line in open(FName):
                line = line.strip()
                vCol = line.split('\t')
                ThisObj = FaccObjC(line)
                self.lObj.append(ThisObj)
                if not ThisObj.Mid in self.hObj:
                    self.hObj[ThisObj.Mid] = 0 
                self.hObj[ThisObj.Mid] += 1
                self.FaccLen += 1
        except IOError:
            print "no facc for [%s]" %(DocNo)
        return
    
        
    def LoadForDoc(self,DocNo):
        self.DocNo = DocNo
        FName = self.MakeFileName(DocNo)
        for line in open(FName):
            line = line.strip()
            vCol = line.split('\t')
            if vCol[0] != DocNo:
                continue
            ThisObj = FaccObjC(line)
            self.lObj.append(ThisObj)
            if not ThisObj.Mid in self.hObj:
                self.hObj[ThisObj.Mid] = 0 
            self.hObj[ThisObj.Mid] += 1
        return
        
    def MakeFileName(self,DocNo):
        vCol = DocNo.split('-')
        FName = self.DataDir + "/" + vCol[1] + "/" + vCol[2] + ".anns.tsv"
        return FName
    
    def MakeFileNameForSplit(self,DocNo):
        vCol = DocNo.split('-')
        FName = self.DataDir + "/" + vCol[1] + "/" + vCol[2] + "/" + DocNo
        return FName
    
    def __deepcopy__(self,memo):
        st = FACCForDoc()
        st.DataDir = self.DataDir
        st.DocNo = self.DocNo
        st.lObj = copy.deepcopy(self.lObj,memo)
        st.hObj = copy.deepcopy(self.hObj,memo)
        st.FaccLen = self.FaccLen
        return st 