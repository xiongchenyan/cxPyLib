'''
Created on Dec 17, 2015 2:06:40 PM
@author: cx

what I do:
    evaluate doc ana ranker
what's my input:

what's my output:


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ExplicitSemanticEncoder')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import logging,json
import math

from EseRank.DocAnaRank.DocAnaRanker import DocAnaRankerC

if __name__=='__main__':
    import sys,os
    from AdhocEva.RankerEvaluator import RankerEvaluatorC
    if 2 != len(sys.argv):
        print 'I evaluate Ana reanker model '
        print 'in\nout'        
        RankerEvaluatorC.ShowConf()
        print 'rankerconf (with format:)'
        print 'a separate config file with format:'
        DocAnaRankerC.ShowConf()
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    
    
    conf = cxConfC(sys.argv[1])   
    QIn = conf.GetConf('in')
    EvaOut = conf.GetConf('out')
    RankerConfIn = conf.GetConf('rankerconf')
    Ranker = DocAnaRankerC(RankerConfIn)
    Evaluator = RankerEvaluatorC(sys.argv[1])
    Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)
