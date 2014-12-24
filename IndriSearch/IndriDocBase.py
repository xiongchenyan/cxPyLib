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
        self.DocNo = "" #doc no
        self.score = 0 #ranking score of indri
        self.lPosition = [] #ints
        self.lTerm = [] #terms
        self.lField = [] #triples:(name,st,ed)
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
        return ' '.join(lTerm)
    
    def GetContent(self):
        lTerm = [self.lTerm[pos].lower() for pos in self.lPosition]
        return ' '.join(lTerm)
    
    
    def GetAnnotation(self):
        return self.lAnnotation    
    
    def SetHField(self):
        for i in range(0,len(self.lField)):
            if not self.lField[i].name in self.hField:
                self.hField[self.lField[i].name] = []
            self.hField[self.lField[i].name].append(i)  
        return True  
        
        
        
        
