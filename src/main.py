#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 21:42:07 2020

@author: pi
"""
from queue import Queue
from Timer import Timer
from Display import Display
from Heater import Heater
from Encoder import Encoder
from Application import Application
    

if __name__ == "__main__":
    A_PIN  = 21
    B_PIN  = 23
    SW_PIN = 22

    A_PIN_2  = 0
    B_PIN_2  = 2
    SW_PIN_2 = 3
    
    display = Display()
    display.init()
    timer = Timer()
    encoder_1 = Encoder(A_PIN,B_PIN,SW_PIN,"encoder_1")
    encoder_2 = Encoder(A_PIN_2,B_PIN_2,SW_PIN_2,"encoder_2")
    heater = Heater()
    application = Application(display,timer,encoder_1,encoder_2,heater)
    
    application.init()
 
