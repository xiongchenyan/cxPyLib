'''
Created on Mar 19, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/GeekTools')
from CrossValidation.ParameterSet import *


'''
SVM Training
    options:
        -s svm_type : set type of SVM (default 0)
            0 -- C-SVC        (multi-class classification)
            1 -- nu-SVC        (multi-class classification)
            2 -- one-class SVM
            3 -- epsilon-SVR    (regression)
            4 -- nu-SVR        (regression)
        -t kernel_type : set type of kernel function (default 2)
            0 -- linear: u'*v
            1 -- polynomial: (gamma*u'*v + coef0)^degree
            2 -- radial basis function: exp(-gamma*|u-v|^2)
            3 -- sigmoid: tanh(gamma*u'*v + coef0)
            4 -- precomputed kernel (kernel values in training_set_file)
        -d degree : set degree in kernel function (default 3)
        -g gamma : set gamma in kernel function (default 1/num_features)
        -r coef0 : set coef0 in kernel function (default 0)
        -c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
        -n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
        -p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
        -m cachesize : set cache memory size in MB (default 100)
        -e epsilon : set tolerance of termination criterion (default 0.001)
        -h shrinking : whether to use the shrinking heuristics, 0 or 1 (default 1)
        -b probability_estimates : whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
        -wi weight : set the parameter C of class i to weight*C, for C-SVC (default 1)
        -v n: n-fold cross validation mode
        -q : quiet mode (no outputs)
'''


class LibSVMParaC:
    def Init(self):
        self.SVMType = 0
        self.KernelType = 0
        self.Degree = 3
        self.Gamma = 1 
        self.Coef = 0
        self.Cost = 1
        self.Nu = 0.5
        self.Epsilon = 0.1
        self.CashSize = 1000
        self.Termination = 0.001
        self.Shrink = 1
        self.ProbEst = 0
        self.Weight = [1,1]
        self.CV=0
        self.Quiet = False
        
        
    def __init__(self):
        self.Init()
        
        
    def dump(self):
        #wi and -v n not implemented
        res = "-s %d -t %d -d %d   " %(self.SVMType,self.KernelType,self.Degree)
        res += '-g %d -r %f -c %f' %(self.Gamma,self.Coef,self.Cost)
        res += '-n %f -p %f -m %d' %(self.Nu,self.Epsilon,self.CashSize)
        res += '-e %f -h %d -b %d' %(self.Termination,self.Shrink,self.ProbEst)
        print "svm para setting [%s]" %(res)
        if self.Quiet:
            res += "-q"
        return res
    
    def SetParameter(self,ParaSet):
        #parameter to set at first version:
            #KernelType
            #Degree
            #Gamma
            #SVMType            
        if 'svmtype' in ParaSet.hPara:
            self.SVMType = int(ParaSet.hPara['svmtype'])
        if 'kerneltype' in ParaSet.hPara:
            self.KernelType = int(ParaSet.hPara['kerneltype'])
        if 'degree' in ParaSet.hPara:
            self.Degree = int(ParaSet.hPara['degree'])
        if 'gamma' in ParaSet.hPara:
            self.Gamma = int(ParaSet.hPara['gamma'])
        if 'cost' in ParaSet.hPara:
            self.Cost = float(ParaSet.hPara['cost'])
        return True
             
             
def ReadSVMParaSet(ParaSetIn):
    lParaSet = ReadParaSet(ParaSetIn)
    lSVMPara = []
    for ParaSet in lParaSet:
        SVMPara = LibSVMParaC()
        SVMPara.SetParameter(ParaSet)
        lSVMPara.append(SVMPara)
    return lSVMPara
             
             