'''
Created on Apr 21, 2014
the base structure for features
features used every where
@author: cx
'''
import json
from copy import deepcopy

class cxFeatureC(object):
    def Init(self):
        self.hFeature = {}
        
    
    def __init__(self,data = ""):
        self.Init()
        if "" == data:
            return        
        if type(data) == str:
            self.loads(data)
    
    
        
    def SetFeature(self,FeatureStr):
        vF = FeatureStr.split('#')
        for feature in vF:
            lMid = feature.split('&')
            if len(lMid) < 2:
                return False
            dim = lMid[0]
            value = float(lMid[1])
            self.hFeature[dim] = value
        return True
    
    def JoinFeatureStr(self):
        FeatureStr = ""
        for item in self.hFeature:
            FeatureStr += item + '&%f#' %(self.hFeature[item])
        return FeatureStr.strip('#')
 
    
    
    def AddFeature(self,hFDict):
#         print "add feature [%s] to [%s]" %(json.dumps(hFDict),self.dumps())
        for item in hFDict:
            if not item in self.hFeature:
                self.hFeature[item] = 0
            self.hFeature[item] += hFDict[item]
#         print "res [%s]" %(self.dumps())
        return True
    
    
    def loads(self,line):
        self.SetFeature(line)
        
    def dumps(self):
        return self.JoinFeatureStr()
    
    
    def __deepcopy__(self,memo):
        Feature = cxFeatureC()
        Feature.hFeature = deepcopy(self.hFeature,memo)
        return Feature
    
    
    def Key(self):
        print "should be implemented by sub class"
        return ""
    
    
    @classmethod
    def LoadFeatureToDict(cls,InName,hFeature = {}):
        #build h{key}->EdgeFeature
        print "start loading feature from [%s]" %(InName)
        for line in open(InName):
            Feature = cls(line.strip())
            if Feature.Key() in hFeature:
#                 print "[%s] in, add new feature" %(Feature.Key())
                hFeature[Feature.Key()].AddFeature(Feature.hFeature)
            else:
                hFeature[Feature.Key()] = Feature
        return hFeature
        
    
    @staticmethod
    def CountFeatureDataAppearance(lData):
        hFeatureCnt = {}
        for data in lData:
            for feature in data.hFeature:
                if not feature in hFeatureCnt:
                    hFeatureCnt[feature] = 1
                else:
                    hFeatureCnt[feature] += 1
        return hFeatureCnt
     
    @staticmethod
    def FilterByFraction(lData,MinFraction = 0.01):
        #filter feature dimension in lData[i] by the minimum appearance fraction
        print "start filter by fraction > [%f]" %(MinFraction)
        hFeatureCnt = cxFeatureC.CountFeatureDataAppearance(lData) 
        MinCnt = len(lData) * MinFraction
        print "feature dim = [%d]" %(len(hFeatureCnt))           
        
        lRes = []
        for data in lData:
            hNewFeature = {}
            for feature in data.hFeature:
                if hFeatureCnt[feature] > MinCnt:
                    hNewFeature[feature] = data.hFeature[feature]
            data.hFeature.clear()
            data.hFeature = hNewFeature
            lRes.append(data)
        
        hResCnt = cxFeatureC.CountFeatureDataAppearance(lRes)
        print "after filter feature dim = [%d]" %(len(hResCnt))    
        return lRes

                    
        
        
    
        
    
