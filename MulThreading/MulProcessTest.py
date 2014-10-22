'''
Created on Oct 21, 2014 9:33:42 PM
@author: cx

what I do:
test mul process
what's my input:

what's my output:


'''


import multiprocessing
import time
import os

class TreadC(object):
    def RunThread(self,TargetTime):
        cnt = 0
        print "sp start"
        while cnt < TargetTime:
            cnt += 1
            time.sleep(1)
            print '[%d] time wait' %(cnt)
        os._exit(0)
            
    def Process(self):
#         if __name__ == '__main__':    
        p = multiprocessing.Process(target=self.RunThread,args=(2,))
        p.start()
        p.join(3)
        
        if p.is_alive():
            print "time out"
            p.terminate()
            
        else:
            print "finish"
                
                
TreadC().Process()
