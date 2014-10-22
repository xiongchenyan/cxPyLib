'''
Created on May 28, 2014
basic operations for texts
@author: cx
'''

lStopWord=["a","about","above","according","across","after","afterwards","again","against","albeit","all","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anywhere","apart","are","around","as","at","av","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","below","beside","besides","between","beyond","both","but","by","can","cannot","canst","certain","cf","choose","contrariwise","cos","could","cu","day","do","does","doesn't","doing","dost","doth","double","down","dual","during","each","either","else","elsewhere","enough","et","etc","even","ever","every","everybody","everyone","everything","everywhere","except","excepted","excepting","exception","exclude","excluding","exclusive","far","farther","farthest","few","ff","first","for","formerly","forth","forward","from","front","further","furthermore","furthest","get","go","had","halves","hardly","has","hast","hath","have","he","hence","henceforth","her","here","hereabouts","hereafter","hereby","herein","hereto","hereupon","hers","herself","him","himself","hindmost","his","hither","hitherto","how","however","howsoever","i","ie","if","in","inasmuch","inc","include","included","including","indeed","indoors","inside","insomuch","instead","into","inward","inwards","is","it","its","itself","just","kind","kg","km","last","latter","latterly","less","lest","let","like","little","ltd","many","may","maybe","me","meantime","meanwhile","might","moreover","most","mostly","more","mr","mrs","ms","much","must","my","myself","namely","need","neither","never","nevertheless","next","no","nobody","none","nonetheless","noone","nope","nor","not","nothing","notwithstanding","now","nowadays","nowhere","of","off","often","ok","on","once","one","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","own","per","perhaps","plenty","provide","quite","rather","really","round","said","sake","same","sang","save","saw","see","seeing","seem","seemed","seeming","seems","seen","seldom","selves","sent","several","shalt","she","should","shown","sideways","since","slept","slew","slung","slunk","smote","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","spake","spat","spoke","spoken","sprang","sprung","stave","staves","still","such","supposing","than","that","the","thee","their","them","themselves","then","thence","thenceforth","there","thereabout","thereabouts","thereafter","thereby","therefore","therein","thereof","thereon","thereto","thereupon","these","they","this","those","thou","though","thrice","through","throughout","thru","thus","thy","thyself","till","to","together","too","toward","towards","ugh","unable","under","underneath","unless","unlike","until","up","upon","upward","upwards","us","use","used","using","very","via","vs","want","was","we","week","well","were","what","whatever","whatsoever","when","whence","whenever","whensoever","where","whereabouts","whereafter","whereas","whereat","whereby","wherefore","wherefrom","wherein","whereinto","whereof","whereon","wheresoever","whereto","whereunto","whereupon","wherever","wherewith","whether","whew","which","whichever","whichsoever","while","whilst","whither","who","whoa","whoever","whole","whom","whomever","whomsoever","whose","whosoever","why","will","wilt","with","within","without","worse","worst","would","wow","ye","yet","year","yippee","you","your","yours","yourself","yourselves"]

hStopWord= dict(zip(lStopWord,lStopWord))

class TextBaseC(object):
    
    @staticmethod
    def RawClean(text):
        #case to lower
        #discard non english, non digit character
        #discard multiple spaces
        
        text= text.lower()
        text = TextBaseC.DiscardNonAlphaNonDigit(text)
        text = ' '.join(text.split())
        return text
        
    
    @staticmethod
    def Uniq(text):
        vCol = text.lower().split()
        return " ".join(list(set(vCol)))
    @staticmethod
    def DiscardNonAlphaNonDigit(s):
        res = ""
        for c in s:
            if (c.isalpha() | c.isdigit() | (c == " ")):
                res += c        
            else:
                res += " "
        return res
    @staticmethod
    def DiscardStopWord(text):    
        vTerm = text.lower().split(' ')
        vRes = []
        for term in vTerm:
            if (term in hStopWord):
                continue
            vRes.append(term)
        return ' '.join(vRes)
    
    
    @staticmethod    
    def DiscardNonAlpha(s):
        res = ""
        for c in s:
            if (c.isalpha() | (c == " ")):
                res += c        
            else:
                res += " "
        return res
    
    @staticmethod
    def TermMatchFrac(texta,textb):
        lA = TextBaseC.RawClean(texta).split()
        lB = TextBaseC.RawClean(textb).split()
        if (len(lA) == 0) | (len(lB) == 0):
            return 0
        score = 0
        
        cnt = 0
        for term in lA:
            if term in lB:
                cnt += 1.0
        score += cnt / float(len(lB))
        cnt = 0.0
        for term in lB:
            if term in lA:
                cnt += 1.0
        score += cnt / float(len(lA))
        score /= 2.0
        return score
        
        
        
    @staticmethod    
    def UW(vCol,hTerm,WindowSize=20, AllowOverlap=False):
        #count the un-ordered count of terms in lTerm appear in text
        if type(hTerm) == list:
            hTerm = dict(zip(hTerm,[0]*len(hTerm)))
        if AllowOverlap:
            return TextBaseC.UWOverlap(vCol,hTerm,WindowSize)
        else:
            return TextBaseC.UWNonOverlap(vCol,hTerm,WindowSize)
    @staticmethod
    def UWOverlap(vCol,hTerm,WindowSize):
        #used terms marked as ""
        #O(n) is OK..    
        cnt = 0    
        for st in range(len(vCol)):
            hMid = dict(hTerm)
            for p in range(st,min(st+WindowSize,len(vCol))):
                if vCol[p] in hMid:
                    del hMid[vCol[p]]
                    vCol[p] = ""                             
            if len(hMid) == 0:
                cnt += 1                        
        return cnt
    
    @staticmethod
    def UWNonOverlap(vCol,hTerm,WindowSize):
        cnt = 0
        st = 0
        while st < len(vCol):
            hMid = dict(hTerm)
            for i in range(st,min(st+WindowSize,len(vCol))):
                if vCol[i] in hMid:
                    del hMid[vCol[i]]
                    if len(hMid) == 0:
                        cnt += 1
                        st = i
                        break
            st += 1      
        return cnt  
    
    
    @staticmethod
    def CoordinateMatchNum(TextA,TextB):
        vColA = TextA.split()
        vColB = TextB.split()
        cnt = 0
        for term in vColA:
            if term in vColB:
                cnt += 1
        return cnt
        
        
        
        