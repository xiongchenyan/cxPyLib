'''
Created on Sep 10, 2013
a function
takes query as input
output the loaded json.
also with accompany function that seg mids from loaded json
@author: cx
'''


import json
import urllib2
import time

RootUrl = 'https://www.googleapis.com/freebase/v1/search?query='



def SearchApiFetcher(query):
    TargetUrl = RootUrl + query.replace(' ','%20')
    print "fetching URL [%s]" %(TargetUrl)
    page = urllib2.urlopen(TargetUrl)
    content = page.read()
    hDict = json.loads(content)
    time.sleep(5)
    if not 'status' in hDict:
        return {}
    if not hDict['status'] == '200 OK':
        return {} 
    return hDict

def SegMachineIdFromSearchApiRes(hApiRes):
    lMachineIdRank = []
    if not 'result' in hApiRes:
        return []
    lResult = hApiRes['result']
    for item in lResult:
        if not 'mid' in item:
            continue
        MidStr = item['mid']
        MidStr = MidStr.replace('/m/','')
        lMachineIdRank.append(MidStr)
    return lMachineIdRank

def SearchApiForMachineIdRanking(query):
    hApiRes = SearchApiFetcher(query)
    return SegMachineIdFromSearchApiRes(hApiRes)


def FetchFbObjFromGoogleAPI(query):
    hRawDict = SearchApiFetcher(query)
    lObj = []
    if 'result' in hRawDict:
        lhObj = hRawDict['result']
        for hObj in lhObj:
            FbObj = FbObjInGoogleAPIC(hObj)
            lObj.append(FbObj)
    print 'Fetched [%d] obj for q [%s]' %(len(lObj),query)
    return lObj
        


class FbObjInGoogleAPIC:
    def Init(self):
        self.ObjId = ""
        self.key = ""
        self.name = ""
        self.NotableName = ""
        
    def __init__(self,hDict = {}):
        self.Init()
        if {} != hDict:
            self.SetFromDict(hDict)
            
    def SetFromDict(self,hDict):
        if 'name' in hDict:
            self.name = hDict['name']
        if 'mid' in hDict:
            mid = hDict['mid']
            lMid = mid.split('/')
            self.ObjId = lMid[len(lMid) - 1]
        if 'id' in hDict:
            self.key = hDict['id']
        if 'notable' in hDict:
            if 'name' in hDict['notable']:
                self.NotableName = hDict['notable']['name']
        return True
            