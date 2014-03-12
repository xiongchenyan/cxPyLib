'''
Created on Mar 11, 2014
ad hoc ranking measure
@author: cx
'''

class AdhocMeasureC:
    
    def Init(self):
        self.map = 0
        self.ndcg = 0
        self.err = 0
        return
    
    
    def __init__(self):
        self.Init()
        
        
    def __deepcopy__(self,memo):
        res = AdhocMeasureC()
        res.map = self.map
        res.ndcg = self.ndcg
        res.err = self.err
        return res
    
    def __add__(self,other):
        res = AdhocMeasureC()
        res.map = self.map + other.map
        res.ndcg = self.ndcg + other.ndcg
        res.err = self.err + other.err
        return res
    def __div__(self,other):
        res = AdhocMeasureC()
        res.map = self.map / other
        res.ndcg = self.ndcg / other
        res.err = self.err / other
        return res
    
    
    def dumps(self,WithName = False):
        if WithName:
            res = "map:%f ndcg:%f err:%f" %(self.map,self.ndcg,self.err)
        else:
            res = "%f %f %f" %(self.map,self.ndcg,self.err)
        return res
    def loads(self,line):
        vCol = line.strip().split()
        if len(vCol) > 3:            
            self.map = float(vCol[0].split(':')[1])
            self.ndcg = float(vCol[1].split(':')[1])
            self.err = float(vCol[2].split(':')[1])
        return True
            
            
        