'''
Created on May 28, 2014
basic operations for texts
@author: cx
'''


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
    def DiscardNonAlpha(s):
        res = ""
        for c in s:
            if (c.isalpha() | (c == " ")):
                res += c        
            else:
                res += " "
        return res
    
        
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