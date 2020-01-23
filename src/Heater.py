# -*- coding: utf-8 -*-
from LPD8806_Python3.raspledstrip.ledstrip import *
import time

class Heater(object):
    
    def __init__(self):
        self.led = LEDStrip(24,True)
    
    def run(self,name):
        print("run heater")
        while True:
                self.led.fillRGB(0,200,i)
                self.led.update()
                print("%d",i)
                time.sleep(0.1)
    

