'''
Created on my MAC Oct 29, 2014-10:14:16 PM
What I do:
Generate various queries
What's my input:
query
What's my output:
change query to different format
@author: chenyanxiong
'''


class QueryGeneratorC(object):
    
    @staticmethod
    def GenerateSDM(query,NearWeight = 0.1, UWWeight = 0.1):
        BOWWeight = 1 - NearWeight - UWWeight
        lTerm = query.split()
        if len(lTerm) == 1:
            return query
        BOWPart = "#combine(" + query + ")"
        
        
        
        lPhase = []
        for i in range(len(lTerm)-1):
            lPhase.append(lTerm[i] + ' ' + lTerm[i+1])
        
            
            
        lNears = ["#1(" + phase + ' ) ' for phase in lPhase]    
        NearPart = "#combine( " + ' '.join(lNears) + ' )'
        
        
        lUWs = ["#uw8(" + phase + ' ) ' for phase in lPhase]    
        UWPart = "#combine( " + ' '.join(lUWs) + ' )'
        
        sdm = '#weight( %.2f '%(BOWWeight) + BOWPart + " %.2f "%(NearWeight) + NearPart + ' %.2f ' %(UWWeight) + UWPart + ")"
        
        return sdm
    
    @staticmethod
    def GenerateMultipleRep(query):
        lTerm = query.split()
        lField = ['url','title','inlink','body']
        lWeight = [0.1,0.2,0.3,0.4]
        
        MulRepQ = '#combine ( '
        
        for term in lTerm:
            MulRepQ += '#wsum( '
            for i in range(len(lField)):
                field = lField[i]
                w = lWeight[i]
                MulRepQ += '%f %s.%s ' %(w,term,field)
            MulRepQ += ') '
        MulRepQ +=') '
        return MulRepQ
    
    @staticmethod
    def GenerateSDMAndMulRep(query,NearWeight = 0.1,UWWeight = 0.1):
        return "#weight(0.5 " + QueryGeneratorC.GenerateSDM(query,NearWeight,UWWeight) + " 0.5 " + QueryGeneratorC.GenerateMultipleRep(query) + ")"
    
        
    
    
