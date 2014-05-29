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