'''
Created on Jan 2, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/Dropbox/workspace/python/Freebase/')
site.addsitedir('/bos/usr4/cx/elementtree-1.2.6-20050316/elementtree')
import sys
import ElementTree as ET #mainly done by xml parser
import json
import xml

#from Base import *

hTypeStrStop={'ns':1,'base':1,'common':1,'topic':1,'user':1,'relationship':1}
hEdgeStrStop={'ns':1,'key':1,'type':1,'object':1,'name':1,'en':1,'rdf':1,'common':1}
hSubqEdge = {'ns:common.topic.alias':1,'key:en':1,'key:wikipedia.en_title':1,'key:wikipedia.en':1,'rdfs:label':1}


hStopEdge={'ns:type.opbject.key':1,'ns:type.object.type':1,'ns:type.type.instance':1,'ns:common.topic.topic_equivalent_webpage':1,'ns:type.object.name':1}

#hReqEdge['ns:common.topic.alias'] = True
#hReqEdge['key:en'] = True
#hReqEdge['key:wikipedia.en_title'] = True
#hReqEdge['key:wikipedia.en'] = True
#hReqEdge['rdfs:label'] = True



class FreebaseObjectC:
    
    def __init__(self,InName = ""):
        self.Init();
        if "" != InName:
            self.parse(InName)
            
    
    def Init(self):
        self.mId = ""
        self.key = ""
        self.name = ""
        self.desp = ""
        self.lEdge = []
        self.hEdge = {}
        self.lType = []
        self.Alias = ""
        self.WikiKey = ""
        self.WikiTitle = ""
        self.subquery = ""
        self.hToDiscardEdge = {}
        self.hToDiscardEdge['ns:type.type.instance'] = True
        self.EdgeCnt=0
        self.ObjEdgeCnt = 0
        self.ConnectObj = []
        
    def parse(self,InName):
#        print "Start parsing [%s]" %(InName)
        try:
            tree = ET.parse(InName)
        except (IOError,xml.parsers.expat.ExpatError):
            print "parse [%s] error" %(InName)
            return False        
#        print 'get [%d] doc' %(len(lNode))
        lNode = tree.findall('./DOC/mid')
        if (len(lNode) > 0):
            self.mId = lNode[0].text
        self.SetEdge(tree)
        self.SetName()
        self.SetAlias()
        self.SetDesp()
        self.SetKey()
        self.GetConnectedObject()
        self.GetType()
        return True
    
    def dump(self,OutName):
        out = open(OutName,"w")
        print >>out,"mid\t"+self.mId
        print >>out,"key\t"+self.key
        print >>out,"name\t"+self.name
        print >>out,"desp\t"+self.desp
        print >>out,json.dumps(self.lEdge)
        return True
    
    def load(self,InName):
        for line in open(InName):
            line = line.strip()
            vCol = line.split('\t')
            if (vCol[0] == 'mid'):
                if (len(vCol) > 1):
                    self.mId = vCol[1]
                continue
            if (vCol[0] == 'key'):
                if (len(vCol) > 1):
                    self.key = vCol[1]
                continue
            if (vCol[0] == 'name'):
                if (len(vCol) > 1):
                    self.name = vCol[1]
                continue
            if (vCol[0] == 'desp'):
                if (len(vCol) > 1):
                    self.desp = vCol[1]
                continue
            self.lEdge = json.loads(line)
            break
        return True
    def GetType(self):
        self.lType = []
        lRes = []
        for edge in self.lEdge:
            if (("ns:type.object.type" == edge[0])  | ("rdf:type" == edge[0])) & (edge[1] != "ns:common.topic"):
                lRes.append(edge[1].replace("ns:",""))
        self.lType = lRes
        return lRes
    
    
    def SetName(self):
        self.name = self.GetTargetEdge("rdfs:label")
        
    def SetDesp(self):
        self.desp = self.GetTargetEdge("ns:common.topic.description")
        
    def SetKey(self):
        self.key = self.GetTargetEdge("key:en")
        
    def SetAlias(self):
        self.Alias = self.GetTargetEdge("ns:common.topic.alias")
    
    def SetWiki(self):
        self.WikiKey = self.GetTargetEdge("key.wikipedia.en")
        self.WikiTitle = self.GetTargetEdge("key.wikepedia.en_title")
    
    
    def GetTargetEdge(self,Target):
        #if have multiple appearance of Target egde, then concatenate them
        TotalText = ""
        for edge in self.lEdge:
            if (edge[0] == Target):
                text,LangTag = self.SegLanguageTag(edge[1])
                if (LangTag == "en") | (LangTag == ""):  
                    TotalText+= text.strip("\"").replace("_"," ").lower() + " "                                                                                                                   
        return TotalText.strip()
    
    def GetConnectedObject(self):
        if (self.ConnectObj == []):
            for edge in self.lEdge:
                if ('ObjectID' in edge[1]):
                    self.ConnectObj.append((edge[0],edge[1][len('ObjectID'):len(edge[1])]))
        return self.ConnectObj
    
    def SetEdge(self,tree):
        #set the self.lEdge from the raw ET tree document
        lNode = tree.findall('./DOC')
        for DocNode in lNode:
            lLinkNode = DocNode.findall('./link')   #will be very big
#            print 'Get [%d] link' %(len(lLinkNode))
            for node in lLinkNode:
                edge = node.text
                if (not self.IsRequiredEdge(edge)):
                    continue;
                self.lEdge.append(edge.split('\t'))                
        return
    
    def IsRequiredEdge(self,edge):
        vCol = edge.split("\t")
        if (len(vCol) < 2):
            return False
        if (vCol[0] in self.hToDiscardEdge):
            return False
        return True
        
        
    def SegLanguageTag(self,s):
        vCol = s.split("@")
        if (len(vCol) < 2):
            return s,""
        else:
            return vCol[0],vCol[1]
    
    def SegObjectID(self,s):
        if (len(s) < 9):
            return ""
        if ('ObjectID' == s[0:8]):
            return s[9:len(s)]
        return ""
        
    
    def MakeHEdge(self):
        for i in range(0,len(self.lEdge)):
            self.hEdge[self.lEdge[i][0]] = i
        return True
    
    
    
    def LoadNeighborText(self,NeighborDir):
        self.NeighborText = ""
        try:
            for line in open(NeighborDir + "/" + self.mId):
                self.NeighborText += line.strip()
        except IOError:
            print "neighbor text for [%s] not exist" %(self.mId)
        return self.NeighborText
    
    
    def LoadTypeText(self,TypeDir):
        self.TypeText = ""
        for TypeName in self.lType:
            try:
                for line in open(TypeDir + "/" + TypeName):
                    self.TypeText += line.strip()
            except IOError:
                print "type text [%s] not exist" %(TypeName)
        return self.TypeText
    
    