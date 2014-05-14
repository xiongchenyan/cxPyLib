'''
Created on May 14, 2014
dfs the graph
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from GraphBase.base import *
from cxBase.base import cxBaseC,cxConf

class DFSerC(cxBaseC):
    def Init(self):
        self.hVisit = {}
        self.Revisit = True
        self.MaxDepth = 4
        return
    
    @staticmethod
    def ShowConf():
        print "revisit\nmaxdepth"
    
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.Revisit = bool(int(conf.GetConf('revisit',1)))
        self.MaxDepth = int(conf.GetConf('maxdepth',self.MaxDepth))
        return True
    
    
    def DFS(self,CurrentNodeId,lPath,Graph):
        #lpath=[(st,ed)]
        if len(lPath) > self.MaxDepth:
            return True
        
        if not self.Revisit:
            if Graph.lNode[CurrentNodeId].Key() in self.hVisit:
                return True
            self.hVisit[Graph.lNode[CurrentNodeId].Key()] = True
        
        self.ProcessCurrentNode(CurrentNodeId,lPath,Graph)
        #deal with curernt node, left for subclass API
        
        Node = Graph[CurrentNodeId]
        for ChildId in Node.hChild:
            self.DFS(ChildId,lPath + [(CurrentNodeId,ChildId)])
        return True
        
        
        
    def ProcessCurrentNode(self,CurrentNodeId,lPath,Graph):
        return True
    