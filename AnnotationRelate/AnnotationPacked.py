'''
Created on Oct 11, 2013
a class to read annotation packed result. stored as FACC1's directory
and to function to match PackedIndriResC with Annotated offset. move bit level to term level
@author: cx
'''

import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')

from IndriRelate.IndriPackedRes import *

class AnnotationPackC:
    DocNo = ""
    encode = ""
    entity = ""
    offset = [0,0]
    posterior = 0
    ContextPost = 0
    MachineId = ""
    
    
    def __init__(self):
        self.DocNo = ""
        self.encode = ""
        self.entity = ""
        self.offset = [0,0]
        self.posterior = 0
        self.ContextPost = 0
        self.MachineId = ""
        
    def Set(self,line):
        vCol = line.strip().split('\t')
        self.DocNo = vCol[0]
        self.encode = vCol[1]
        self.entity = vCol[2]
        self.offset[0] = int(vCol[3])
        self.offset[1] = int(vCol[4])
        self.posterior = float(vCol[5])
        self.ContextPost = float(vCol[6])
        self.MachineId = vCol[7]
        return
    
    
    
def ReadAnnotation(InName):
    lAnnotationPack = []
    for line in open(InName):
        AnPack = AnnotationPackC()
        AnPack.Set(line)
        lAnnotationPack.append(AnPack)
    return lAnnotationPack


def MakeDocRangeInAnnotation(lAnnotation):
    lDocRange = []
    st = 0
    ed = 0
    for i in range(1,len(lAnnotation)):
        if lAnnotation[i].DocNo != lAnnotation[i - 1].DocNo:
            ed = i
            lDocRange.append([st,ed])
            st = ed
    lDocRange.append([st,len(lAnnotation)])
    return lDocRange 


def SplitAnnotationForDoc(lAnnotationPack,DocNo):
    lRes = []
    for pack in lAnnotationPack:
        if pack.DocNo == DocNo:
            lRes.append(pack)
    return lRes


def StringMatchOffSet(Annotation, PackedDoc):
    #PackedDoc must have DocRaw
    #do raw string containment in DocRaw and entity
    #not sure whether stemmed or not.
    entity = Annotation.entity.lower()
    RawDoc = PackedDoc.RawContent.lower()
    lIndex = []
    st = 0;
    while True:
        p = RawDoc.find(entity,st)
        if -1 == p:
            break
        lIndex.append((p,p + len(entity)))
        st += p + len(entity)
        
    return lIndex

def DocVecMatchOffset(Annotation, PackedDoc):
    #match with docvec
    content = PackedDoc.GetContent()
    entity = Annotation.entity.lower()
    lIndex = []
    st = 0;
    while True:
        p = content.find(entity,st)
        if -1 == p:
            break
        st += p + len(entity)
        lIndex.append((st,st + len(entity)))
    return lIndex

def ShowStrAtOffset(Annotation, PackedDoc,AdditionalLen = 0):
    #show string at offset
    st = Annotation.offset[0]-AdditionalLen
    ed = Annotation.offset[1] + AdditionalLen
    return PackedDoc.RawContent[st:ed]


def MakeAnnotationName(InitDir, DocNo):
    vCol = DocNo.split('-')
    DirName = vCol[1]
    FileName = vCol[2] + '.anns.tsv'
    return InitDir + "/" + DirName + "/" + FileName



    
    
    
    
    
        
        
    
