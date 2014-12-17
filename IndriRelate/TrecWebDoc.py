'''
Created on Dec 16, 2014 7:15:45 PM
@author: cx

what I do:
I am the base class for TrecWeb document
what's my input:
support multiple type:
    Oshmued
what's my output:
TrecWeb format data

'''

class TrecWebDocC(object):
    def __init__(self,lData = []):
        self.DocNo = ""
        self.lField = []  #(fieldname, field text)
        self.Url = ""
        if [] != lData:
            if type(lData) == list:
                if '.I' == lData[0][:2]:
                    self.LoadOhsumedDoc(lData)
        
    def dumps(self):
        res = "<DOC>\n"
        res += "<DOCNO>%s</DOCNO>\n" %(self.DocNo)
        res += "<DOCHDR>\n%s\n</DOCHDR>\n" %(self.Url)
        for field in self.lField:
            res += "<%s>\n%s</%s>\n" %(field[0],field[1],field[2])
        res += "</DOC>"
        return res
    
    def LoadOhsumedDoc(self,lLines):
        for i in range(1,len(lLines)):
            if lLines[i - 1] == '.U':
                self.DocNo = lLines[i]
            if lLines[i - 1] == '.T':
                self.lField.append['title',lLines[i]]
            if lLines[i - 1] == '.W':
                self.lField.append(['body',lLines[i]])
        return
    
    
