'''
Created on Oct 28, 2014 4:59:12 PM
@author: cx

what I do:
I am the base class for indri doc
Goal is to replace the unnecessarily complicated IndriPackedRes
to be used for the whole SemanticSearch

see, so simple!
what's my input:

what's my output:


'''

import json
import copy

class IndriDocBaseC(object):
    def __init__(self,hData = {}):
        self.Init()
        if {} != hData:
            self.SetFromDict(hData)
        
    def Init(self):
        #stuff that returned by indri api
        self.DocNo = "" #doc no
        self.score = 0 #ranking score of indri
        self.lPosition = [] #ints
        self.lTerm = [] #terms
        self.lField = [] #triples:(name,st,ed)
        
        #stuff that is added
        self.hField = {}
        self.lAnnotation = []
        
    def SetFromDict(self,hData):
        for key in hData.keys():
            setattr(self, key, hData[key])
        
    
    def dumps(self):
        return json.dumps(self.__dict__)
    
    def loads(self,text):
        '''
        c program's output should be able to be loaded from this as well
        '''
        self.__dict__ = json.loads(text)
        
    
    def OOVFraction(self):
        if [] == self.lPosition:
            return 0
        OOVP = -1
        for i in range(len(self.lTerm)):
            if self.lTerm[i] == '[OOV]':
                OOVP = i
                break
            
        OOVCnt = len([p for p in self.lPosition if p == OOVP])
        return float(OOVCnt) / float(len(self.lPosition))
        
        
        
    @staticmethod
    def MulLoads(text):
        lData = json.loads(text)
        lDoc = []
        for data in lData:
            doc = IndriDocBaseC(data)
            lDoc.append(doc)
        return lDoc
    
    def GetField(self,FieldName):
        lPos = []
        for Field in self.lField:
            if Field[0] == FieldName:
                lPos.extend(self.lPosition[Field[1]:Field[2]])
                
        lTerm = [self.lTerm[pos] for pos in lPos]
        return ' '.join(lTerm).encode('ascii','replace')
    
    def GetContent(self):
        lTerm = [self.lTerm[pos].lower() for pos in self.lPosition]
        return ' '.join(lTerm).encode('ascii','replace')
    
    
    def GetAnnotation(self):
        return self.lAnnotation    
    
    def SetHField(self):
        for i in range(0,len(self.lField)):
            if not self.lField[i][0] in self.hField:
                self.hField[self.lField[i][0]] = []
            self.hField[self.lField[i][0]].append(i)  
        return True  
        
        
        
        
