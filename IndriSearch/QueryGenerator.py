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
    def GenerateSDM(query):
        lTerm = query.split()
        if len(lTerm) == 1:
            return query
        BOWPart = "#AND(" + query + ")"
        
        
        
        lPhase = []
        for i in range(len(lTerm)-1):
            lPhase.append(lTerm[i] + ' ' + lTerm[i+1])
        
            
            
        lNears = ["#NEAR/1(" + phase + ' ) ' for phase in lPhase]    
        NearPart = "#AND( " + ' '.join(lNears) + ' )'
        
        
        lUWs = ["#WINDOW/8(" + phase + ' ) ' for phase in lPhase]    
        UWPart = "#AND( " + ' '.join(lUWs) + ' )'
        
        sdm = '#WAND( 0.8 ' + BOWPart + " 0.1 " + NearPart + ' 0.1 ' + UWPart + ")"
        
        return sdm
    
    @staticmethod
    def GenerateMultipleRep(query):
        lTerm = query.split()
        lField = ['url','title','inlink','body']
        lWeight = [0.1,0.2,0.3,0.4]
        
        MulRepQ = '#AND ( '
        
        for term in lTerm:
            MulRepQ += '#WSUM( '
            for i in range(len(lField)):
                field = lField[i]
                w = lWeight[i]
                MulRepQ += '%f %s.%s ' %(w,term,field)
            MulRepQ += ') '
        MulRepQ +=') '
        return MulRepQ
    
    @staticmethod
    def GenerateSDMAndMulRep(query):
        return "#WAND(0.5 " + QueryGeneratorC.GenerateSDM(query) + " 0.5 " + QueryGeneratorC.GenerateMultipleRep(query) + ")"
    
        
    
    
