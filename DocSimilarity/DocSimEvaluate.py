'''
Created on Aug 28, 2015 7:54:12 PM
@author: cx

what I do:
    I evaluate doc similarity
what's my input:
    LP data in
    a function that takes [DocNo,text] * 2 as input, and return a similarity score
    
what's my output:
    Pearson correlation with doc labels
'''


import site
import logging


site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import numpy as np
from scipy.stats import pearsonr
from cxBase.TextBase import TextBaseC

class DocSimEvaluatorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.lText = []
        self.lDocNo = []
        self.lSimScore = []
        
        self.TextIn = ""
        self.LabelIn = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn) 
        self.TextIn = self.conf.GetConf('textin')
        self.LabelIn = self.conf.GetConf('labelin')
        
        self.LoadDocSimData()
        
        
    def LoadDocSimData(self):
        lLines = open(self.TextIn).read().splitlines()
        
        self.lDocNo = [line.split('\t')[0] for line in lLines]
        
        lText = [line.split('\t')[1].split('(')[0] for line in lLines]
        lText = [TextBaseC.RawClean(line) for line in lText]
        self.lText = lText
        
        
        lLines = open(self.LabelIn).read().splitlines()
        lvCol = [line.split(',') for line in lLines]
        lvCol = [[float(item) for item in vCol] for vCol in lvCol]

        lvCol.sort(key= lambda item: (item[0],item[1]))
        self.lSimScore = lvCol
            
        logging.info('load doc sim data finished')
        return True
    
    
    def PearsonCorr(self,lPreRes):
        
        lLabel = [item[2] for item in self.lSimScore]
        lPredict = [item[2] for item in lPreRes]
        pearson,p = pearsonr(lLabel,lPredict)
        return pearson
    
    
    def EvaluateSimFunc(self,SimFunc):
        
        lPreRes = []        
        for i in range(len(self.lText)):
            for j in range(i+1,len(self.lText)):
                score = SimFunc([self.lDocNo[i],self.lText[i]],[self.lDocNo[j],self.lText[j]])
                lPreRes.append([i+1,j+1,score])
                
        score = self.PearsonCorr(lPreRes)
        logging.info('sim func doc sim pearson: %f',score)
        return score
        
        
        
        
