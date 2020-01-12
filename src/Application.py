# -*- coding: utf-8 -*-

from Display import Display
from Timer import Timer
from enum import Enum
from queue import Queue
import threading
import time

BREAD_IMAGE = '../assets/bread.jpg'
ZOPF_IMAGE = '../assets/zopf.jpg'
BANANE_IMAGE = '../assets/banane.png'


class Application_State(Enum):
    Init = 0
    Menu_Dialog = 1
    Timer_Setting = 2
    Timer_Countdown = 3


class Application(object):
    
    def __init__(self,Display,Timer,Encoder_1,Encoder_2):
        self.application_state = Application_State.Init
        self.display = Display
        self.timer = Timer
        self.encoder_1 = Encoder_1
        self.encoder_2 = Encoder_2
        self.encoder_1_queue = Queue(maxsize=1)
        self.encoder_2_queue = Queue(maxsize=1)
        self.encoder_1_thread = threading.Thread(
                target=self.encoder_1.run, args=(self.encoder_1_queue,))
        self.my_own_thread = threading.Thread(
                target=self.run, args=(1,))
        
    def state_machine(self):
        if self.application_state == Application_State.Init:
            self.display.init()
            self.timer.set_update_callback(self.display.show_timer_screen)
        if self.application_state == Application_State.Menu_Dialog:
            print("")
        if self.application_state == Application_State.Timer_Countdown:
            self.timer.set_update_callback(self.display.show_timer_screen)
            self.timer.start()
    
    def handle_peripherals(self):
        try:
            message_encoder_1 = self.encoder_1_queue.get_nowait()
            print(message_encoder_1['type'])
            print(message_encoder_1['value'])
            self.encoder_1_queue.task_done()
        except:
            print("empty")
            
    def init(self):
        self.encoder_1_thread.start()
        self.my_own_thread.start()
        
    def run(self,name):
        while True:
            print("hello")
            time.sleep(1)
            self.handle_peripherals()
            
        