'''
Created on Jan 9, 2014
creat and make authority data center
@author: cx
'''

import pickle
import math

class InLinkCenterC:
    def Init(self):
        self.hInLink = {}
        
        
    def __init__(self):
        self.Init()
        
        
    def LoadFromEdgeData(self,ObjIdIn,ObjEdgeIn):
        self.hInLink = {}
        for line in open(ObjIdIn):
            line = line.strip()
            self.hInLink[line] = 0
        for line in open(ObjEdgeIn):
            vCol = line.strip().split('\t')
            if vCol[1] in self.hInLink:
                self.hInLink[vCol[1]] += 1
        return True
    
    def Dump(self,OutName):
        out = open(OutName,"w")
        pickle.dump(self.hInLink,out)
        out.close()
        return True
    
    def Load(self,InName):
        In = open(InName,'r')
        self.hInLink = pickle.load(In)
        In.close()
        return True
    
    def GetInLink(self,ObjId):
        InCnt = 0
        MinCnt = 1
        if ObjId in self.hInLink:
            InCnt = self.hInLink[ObjId]
        return math.log(max(InCnt,MinCnt))
    


# 
# import sys
# 
# #sys used to make inlink file
#     
# if 4 != len(sys.argv):
#     print "3 para: ObjIdIn + ObjEdgeIn + outname"
#     sys.exit()
#     
# InLinkCenter = InLinkCenterC()
# InLinkCenter.LoadFromEdgeData(sys.argv[1], sys.argv[2])
# InLinkCenter.Dump(sys.argv[3])