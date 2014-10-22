'''
Created on Oct 21, 2014 9:26:13 PM
@author: cx

what I do:
test Multi threading
what's my input:
none
what's my output:
none

'''



import threading
import time

def RunThread(TargetTime):
    cnt = 0
    while cnt < TargetTime:
        cnt += 1
        time.sleep(1)
    return 1



p = threading.thread()