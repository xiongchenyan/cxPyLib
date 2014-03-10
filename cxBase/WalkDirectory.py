'''
Created on Oct 16, 2013
given a dirname, return all its files
@author: cx
'''



import os

def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName
        