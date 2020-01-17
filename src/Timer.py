# -*- coding: utf-8 -*-
import time
import threading

class Timer(object):
    def __init__(self):
        self.remaining_time_s = 0
        self.callback = None
        self.stopThread = False
        
    def set_remaining_time_s(self,seconds):
        self.remaining_time_s = seconds
        
    def get_remaining_time_s(self):
        return self.remaining_time_s
    
    def start(self):
        print("Timer start")
        self.t = threading.Thread(target=self._count_down)
        self.t.daemon = True
        self.stopThread = False
        self.t.start()
        
    def stop(self):
        print("Timer stop")
        self.stopThread = True
        self.t.kill()
            
    def _count_down(self):
        while self.remaining_time_s > 0 and not self.stopThread:
            self.remaining_time_s -= 1
            self.callback(self.remaining_time_s)
            time.sleep(1)
            
    def set_update_callback(self,callback):
        self.callback = callback
        
        