'''
Created on Mar 25, 2014
input: train, dev|test, para
output: accuracy, label of required
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')
site.addsitedir('/bos/usr0/cx/LibSVM/libsvm/python/')
from LibSVMRelate.SVMBase import *
from svmutil import *
from cxBase.base import *
import json

class SVMRunSingleParaC(object):
    
    def LoadData(self,InName):
        print "to be implemented by my inherited class"
        return [[],[]]
    
    def DumpPrediction(self,OutName,TestInName ,p_label,p_val):
        print "to be implemented by my inherited class"
        return False
    
    def Process(self,TrainInName,TestInName,ParaInName,OutName):
        
        lY,lX = self.LoadData(TrainInName)
        lSVMPara = ReadSVMParaSet(ParaInName)
        SVMPara = lSVMPara[0] #only use first one
        
        SVMModel = svm_train(lY,lX,SVMPara.dump())
        
        lTestY,lTestX = self.LoadData(TestInName)
        p_label,p_acc,p_val = svm_predict(lTestY,lTestX,SVMModel,'-b 1')
        
        out = open(OutName,'w')
        json.dump(p_acc,out)       
        self.DumpPrediction(OutName + "_pre", TestInName, p_label, p_val)        
        return True
