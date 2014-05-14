'''
Created on May 14, 2014
basic class for node,and graph
@author: cx
'''

from copy import deepcopy

class NodeC(object):
    def Init(self):
        self.name=""
        self.id = 0
        self.lAttr=[] #node attr
        self.hChild = {} #id->[edge attr], each item is an edge between they two
        
    def __init__(self,name="",lAttr=[]):
        self.Init()
        self.name = name
        self.lAttr = list(lAttr)
        
    def AddChild(self,NodeId,lEdgeAttr):
        if not NodeId in self.hChild:
            self.hChild[NodeId] = []
        self.hChild[NodeId].append(lEdgeAttr)
        return True
    
    
    def Key(self):
        return self.name
    
    def __deepcopy__(self,memo):
        res = NodeC()
        for key,item in self.__dict__.items():
            if key.startwith('__'):
                continue
            res.__dict__[key] = deepcopy(item,memo)
        return res
    
    
class GraphC(object):
    def Init(self):
        self.lNode = [] #list of nodes
        self.hNode = {}
        
    def __deepcopy__(self,memo):
        graph = GraphC()
        graph.lNode = deepcopy(self.lNode,memo)
        graph.hNode = deepcopy(self.hNode,memo)
        return graph
    
    def empty(self):
        return len(self.lNode) == 0
    
    def __init__(self,graph=""):
        self.Init()
        if type(graph).__name__ == 'GraphC':
            self = deepcopy(graph)

    def AddNode(self,Node):
        if not Node.Key() in self.hNode:
            self.lNode.append(Node)
            self.lNode[len(self.lNode)-1].id = len(self.lNode) - 1
            self.hNode[Node.Key()] = len(self.lNode) - 1
        p = self.hNode[Node.Key()]
        for att in Node.lAttr:
            if not att in self.lNode[p].lAttr:
                self.lNode[p].lAttr.extend(att)
        return True
                
    
    def AddEdge(self,StName,EdName,lEdgeAttr):
        if not StName in self.hNode:
            Node = NodeC(StName)
            self.AddNode(Node)
        if not EdName in self.hNode:
            Node = NodeC(EdName)
            self.AddNode(Node)
        StId = self.hNode[StName]
        EdId = self.hNode[EdName]
        self.lNode[StId].AddChild(EdId,lEdgeAttr)
        return True
    
    def clear(self):
        self.hNode.clear()
        del self.lNode[:]


    def GetReverse(self):
        Graph = deepcopy(self)
        for i in range(len(Graph.lNode)):
            Graph.lNode[i].hChild.clear()
        
        for i in range(len(self.lNode)):
            for j in self.lNode[i].hChild:
                for lEdgeAttr in self.lNode[i].hChild[j]:
                    StName = self.lNode[i].name
                    EdName = self.lNode[j].name
                    Graph.AddEdge(EdName,StName,lEdgeAttr)
        return Graph
        
    def ReadFromSimpleEdgeFile(self,InName):
        #format: node\tnode\tedge name\tweight
        try:
            for line in open(InName):
                vCol = line.strip().split('\t')
                lEdgeAttr = [vCol[2],float(vCol[3])]
                self.AddEdge(vCol[0], vCol[1], lEdgeAttr)
        except IOError:
            print "file [%s] not exist" %(InName)
            return False
        return True
    
    def OutSimpleEdgeFile(self,OutName):
        out = open(OutName,'w')
        for node in self.lNode:
            for ChildId in node.hChild:
                StName = node.name
                EdName = self.lNode[ChildId].name
                for lEdgeAttr in node.hChild[ChildId]:
                    print >>out, StName + "\t" + EdName + "\t" + lEdgeAttr[0] + "\t%f" %(lEdgeAttr[1])
        out.close()
        return True
    
    def DiscardNoneTargetEdge(self,hTargetEdge):
        #discard edge that is not in htarget
        TotalCnt = 0
        for i in range(len(self.lNode)):
            lToDel = []
            for j in self.lNode[i].hChild:
                TotalCnt += 1
                if not (i,j) in hTargetEdge:
                    lToDel.append(j)
            for child in lToDel:
                self.DeleteEdge((i,child))
        print "keep [%d] edge from [%d]" %(len(hTargetEdge),TotalCnt)
        return True
    
    
    
    def DeleteEdge(self,edge):
        del self.lNode[edge[0]].hChild[edge[1]]
        
        
        
                    
    
        
        
        
        