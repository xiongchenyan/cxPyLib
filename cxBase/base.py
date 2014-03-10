'''
Created on Jun 17, 2013

@author: cx
'''
import re, math
import sys
from collections import Counter
import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
from nltk import PorterStemmer


lStopWord=["a","about","above","according","across","after","afterwards","again","against","albeit","all","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anywhere","apart","are","around","as","at","av","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","below","beside","besides","between","beyond","both","but","by","can","cannot","canst","certain","cf","choose","contrariwise","cos","could","cu","day","do","does","doesn't","doing","dost","doth","double","down","dual","during","each","either","else","elsewhere","enough","et","etc","even","ever","every","everybody","everyone","everything","everywhere","except","excepted","excepting","exception","exclude","excluding","exclusive","far","farther","farthest","few","ff","first","for","formerly","forth","forward","from","front","further","furthermore","furthest","get","go","had","halves","hardly","has","hast","hath","have","he","hence","henceforth","her","here","hereabouts","hereafter","hereby","herein","hereto","hereupon","hers","herself","him","himself","hindmost","his","hither","hitherto","how","however","howsoever","i","ie","if","in","inasmuch","inc","include","included","including","indeed","indoors","inside","insomuch","instead","into","inward","inwards","is","it","its","itself","just","kind","kg","km","last","latter","latterly","less","lest","let","like","little","ltd","many","may","maybe","me","meantime","meanwhile","might","moreover","most","mostly","more","mr","mrs","ms","much","must","my","myself","namely","need","neither","never","nevertheless","next","no","nobody","none","nonetheless","noone","nope","nor","not","nothing","notwithstanding","now","nowadays","nowhere","of","off","often","ok","on","once","one","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","own","per","perhaps","plenty","provide","quite","rather","really","round","said","sake","same","sang","save","saw","see","seeing","seem","seemed","seeming","seems","seen","seldom","selves","sent","several","shalt","she","should","shown","sideways","since","slept","slew","slung","slunk","smote","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","spake","spat","spoke","spoken","sprang","sprung","stave","staves","still","such","supposing","than","that","the","thee","their","them","themselves","then","thence","thenceforth","there","thereabout","thereabouts","thereafter","thereby","therefore","therein","thereof","thereon","thereto","thereupon","these","they","this","those","thou","though","thrice","through","throughout","thru","thus","thy","thyself","till","to","together","too","toward","towards","ugh","unable","under","underneath","unless","unlike","until","up","upon","upward","upwards","us","use","used","using","very","via","vs","want","was","we","week","well","were","what","whatever","whatsoever","when","whence","whenever","whensoever","where","whereabouts","whereafter","whereas","whereat","whereby","wherefore","wherefrom","wherein","whereinto","whereof","whereon","wheresoever","whereto","whereunto","whereupon","wherever","wherewith","whether","whew","which","whichever","whichsoever","while","whilst","whither","who","whoa","whoever","whole","whom","whomever","whomsoever","whose","whosoever","why","will","wilt","with","within","without","worse","worst","would","wow","ye","yet","year","yippee","you","your","yours","yourself","yourselves"]

hStopWord= dict(zip(lStopWord,lStopWord))


WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def TextCosine(text1,text2):
    vector1 = text_to_vector(PorterStemmer().stem_word(text1.lower()))
    vector2 = text_to_vector(PorterStemmer().stem_word(text2.lower()))
    cosine = get_cosine(vector1, vector2)
    return cosine




def SubCont(phrase,text):
    if (len(phrase) < 1):
        return 0
    return float(text.lower().count(phrase.lower()))


def PortStem(text):
    vCol = text.split()
    for i in range(0,len(vCol)):
        vCol[i] = PorterStemmer().stem_word(vCol[i])
    return ' '.join(vCol)

def Uniq(text):
    vCol = text.lower().split()
    return " ".join(list(set(vCol)))
def DiscardNonAlphaNonDigit(s):
    res = ""
    for c in s:
        if (c.isalpha() | c.isdigit() | (c == " ")):
            res += c        
        else:
            res += " "
    return res
    
def DiscardNonAlpha(s):
    res = ""
    for c in s:
        if (c.isalpha() | (c == " ")):
            res += c        
        else:
            res += " "
    return res    
    
class cxConf:

    
    def __init__(self,InName):
        self.hConf = {}
        if (InName != ""):
            self.LoadConf(InName)
        return
    
    def LoadConf(self,InName):
        for line in open(InName):
            vCol = line.strip().split(" ")
            if (len(vCol) < 2):
                continue
            lConfValue = vCol[1].split('#')
            if 1 == len(lConfValue):
                self.hConf[vCol[0].lower()] = vCol[1]
            else:
                self.hConf[vCol[0].lower()] = lConfValue #support multiple value now
        return True
    
    def GetConf(self,name):
        name = name.lower()
        if (not name in self.hConf):
            return ""
        return self.hConf[name] 
WORD = re.compile(r'\w+')

#read label from labeled data file, make qid#mid pairs if postive
def FbObjLabelLoader(InName):
    hLabel={}
    for line in open(InName):
        vCol = line.strip().split('\t')
        MachineId = vCol[3]
        qid = vCol[0]
        if (MachineId == '#empty#'):
            continue
        hLabel[qid + "#" + MachineId] = True
    return hLabel


def KLDivergence(lProbA,lProbB):
    #KL divergence KL(A,B)
    #normalize A and B first
    #then sum_i lProb[i] log(lProbA[i]/lProbB[i])
    res = 0
    lA = NormalizeProb(lProbA)
    lB = NormalizeProb(lProbB)
    if len(lProbA) != len(lProbB):
        print "fatal! KL divergence two multinomial distribution has diff dimension"
    for i in range(len(lA)):
        res += lA[i] * math.log(lA[i] / lB[i])    
    return res
    
def NormalizeProb(lProb):
    Total = 0
    for prob in lProb:
        Total += prob
    if Total == 0:
        return lProb
    if Total == 1:
        return lProb
    lRes = []
    for i in range(len(lProb)):
        lRes.append(lProb[i] / Total)
    return lRes


def FilterNonEnglishStrInFb(InStr):
    res = ""
    flag = 0
    for c in InStr:
        if (c == '$'):
            flag = 1
            continue
        if (c.isalpha()):
            flag = 1
        if (flag & c.isdigit()):
            continue
        res += c
    return res

def TermsAroundTargetString(text,TargetStr,WindowSize):
    lRes = []
    text = text.lower()
    PreLen = WindowSize / 2
    SufLen = WindowSize / 2
    TargetStr = TargetStr.lower()
    if (not TargetStr in text):
        return lRes
    p = text.index(TargetStr)
    MinP = max(0,p - PreLen)
    MaxP = min(len(text),p + SufLen)
    vTerm = text[MinP:MaxP].split()
    if (len(vTerm) < 2):
        return lRes
    lRes = vTerm[1:len(vTerm)-1]
    return lRes

def ContainNonLetter(s):
    for c in s:
        if not c.isalpha():
            return True
    return False

def DiscardStopWord(text):    
    vTerm = text.lower().split(' ')
    vRes = []
    for term in vTerm:
        if (term in hStopWord):
            continue
        vRes.append(term)
    return ' '.join(vRes)
