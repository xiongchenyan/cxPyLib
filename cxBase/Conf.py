'''
Created on Jun 4, 2014
movie conf class from base.py
rename it as cxConfC
modify some api
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')

import json
from copy import deepcopy
    
class cxConfC(object):
    
    def Init(self):
        self.hConf = {}    
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    
    def SetConf(self,InName):
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
    
    def GetConf(self,name,DefaultValue = ""):
        name = name.lower()
        if (not name in self.hConf):
            print "conf [%s] not exist" %(name)
            return DefaultValue
        print "get conf [%s] [%s]" %(name,json.dumps(self.hConf[name]))
        
        if type(DefaultValue) != type(self.hConf[name]):
            return type(DefaultValue)(self.hConf[name])
        
        return self.hConf[name] 
    
    def SetField(self,name,value):
        self.hConf[name] = value
        return True
    
    def dump(self,OutName):
        out = open(OutName,'w')
        for item in self.hConf:
            value = self.hConf[item]
            if type(value) == list:
                print >>out,item + " %s" %('#'.join([str(mid) for mid in value]))
            else:
                print >> out, item + " " + value
        out.close()
        return True
    
    
    def __deepcopy__(self,memo):
        conf = cxConfC()
        conf.hConf = deepcopy(self.hConf)
        return conf



if __name__ == '__main__':
    import logging
    import sys
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    print "I am the conf class, please import me for futher usage"
    
    
    root.addHandler(ch)