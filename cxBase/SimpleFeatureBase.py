'''
Created on Dec 29, 2014 8:50:27 PM
@author: cx

what I do:
I provide simple operations for dict style feature
    min-max normalization
    add minimum value for missing feature
    support one,two, three dimension list of feature
what's my input:

what's my output:


'''
import itertools
from copy import deepcopy
class SimpleFeatureBaseC(object):
    
    @staticmethod
    def MinFeatureValue(lFeature):
        hMin = {}
        for hFeature in lFeature:
            for key,value in hFeature.items():
                if not key in hMin:
                    hMin[key] = value
                else:
                    hMin[key] = min(value,hMin[key])
        return hMin
    
    @staticmethod
    def MaxFeatureValue(lFeature):
        hMax = {}
        for hFeature in lFeature:
            for key,value in hFeature.items():
                if not key in hMax:
                    hMax[key] = value
                else:
                    hMax[key] = min(value,hMax[key])
        return hMax
    
     
    @staticmethod
    def AddMinForMissingFeature(lFeature):
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        for i in range(len(lFeature)):
            hMid = dict(hMin)
            hMid.update(lFeature[i])
            lFeature[i] = dict(hMid)
        return lFeature
    
    
    @staticmethod
    def MinMaxNormalization(lFeature):
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        hMax = SimpleFeatureBaseC.MaxFeatureValue(lFeature)
        
        hDiff = {hMax[key] - value for key,value in hMin.items()}
        
        for i in range(len(lFeature)):
            hFeature = lFeature[i]
            for key,value in hFeature.items():
                diff = hDiff[key]
                if diff == 0:
                    continue
                hFeature[key] = (value - hMin[key]) / float(diff)
            lFeature[i] = hFeature
        return lFeature
      
      
    @staticmethod
    def AddMinForMissingFeatureTwoDim(llFeature):
        lFeature = list(itertools.chain(*llFeature))
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        for i in range(len(llFeature)):
            for j in range(len(llFeature[i])):
                hMid = dict(hMin)
                hMid.update(llFeature[i][j])
                llFeature[i][j] = dict(hMid)
        return llFeature
    
    
    @staticmethod
    def MinMaxNormalizationTwo(llFeature):
        lFeature = list(itertools.chain(*llFeature))
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        hMax = SimpleFeatureBaseC.MaxFeatureValue(lFeature)
        
        hDiff = {hMax[key] - value for key,value in hMin.items()}
        
        for i in range(len(llFeature)):
            for j in range(len(llFeature[i])):
                hFeature = llFeature[i][j]
                for key,value in hFeature.items():
                    diff = hDiff[key]
                    if diff == 0:
                        continue
                    hFeature[key] = (value - hMin[key]) / float(diff)
                llFeature[i] = hFeature
        return llFeature
    
    
    @staticmethod
    def AddMinForMissingFeatureThree(lllFeature):
        lFeature = list(itertools.chain(*list(itertools.chain(*lllFeature))))
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        for i in range(len(lllFeature)):
            for j in range(len(lllFeature[i])):
                for k in range(len(lllFeature[i][j])):
                    hMid = dict(hMin)
                    hMid.update(lllFeature[i][j][k])
                    lllFeature[i][j][k] = dict(hMid)
        return lllFeature
    
    
    @staticmethod
    def MinMaxNormalizationThree(lllFeature):
        lFeature = list(itertools.chain(*list(itertools.chain(*lllFeature))))
        hMin = SimpleFeatureBaseC.MinFeatureValue(lFeature)
        hMax = SimpleFeatureBaseC.MaxFeatureValue(lFeature)
        
        hDiff = {hMax[key] - value for key,value in hMin.items()}
        
        for i in range(len(lllFeature)):
            for j in range(len(lllFeature[i])):
                for k in range(len(lllFeature[i][j])):
                    hFeature = lllFeature[i][j][k]
                    for key,value in hFeature.items():
                        diff = hDiff[key]
                        if diff == 0:
                            continue
                        hFeature[key] = (value - hMin[key]) / float(diff)
                    lllFeature[i][j][k] = hFeature
        return lllFeature
      
      
        
#     @staticmethod
#     def ConvertToOneDimList(data):
#         '''
#         convert input multi-dim list into one dim
#         '''
#         mid = deepcopy(data)
#         while (type(mid[0]) == list):
#             mid = list(itertools.chain(*mid))
#         return mid
#     
#     @staticmethod
#     def BackToMulDim(data,lFeature):
#         '''
#         convert lFeature back to data
#         '''
        
        
        
    
    
    
