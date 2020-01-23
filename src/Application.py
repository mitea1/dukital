# -*- coding: utf-8 -*-

from Display import Display
from Timer import Timer
from Heater import Heater
from enum import Enum
from queue import Queue, LifoQueue
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
    Temperature_Setting = 4


class Application(object):
    
    def __init__(self,Display,Timer,Encoder_1,Encoder_2,Heater):
        self.application_state = Application_State.Init
        self.display = Display
        self.timer = Timer
        self.encoder_1 = Encoder_1
        self.encoder_2 = Encoder_2
        self.heater = Heater
        self.encoder_1_queue = LifoQueue(maxsize=1)
        self.encoder_2_queue = Queue(maxsize=1)
        self.encoder_1_thread = threading.Thread(
                target=self.encoder_1.run, args=(self.encoder_1_queue,))
        self.encoder_2_thread = threading.Thread(
                target=self.encoder_2.run, args=(self.encoder_1_queue,))
        self.heater_thread = threading.Thread(
                target=self.heater.run, args=(1,))
        self.my_own_thread = threading.Thread(
                target=self.run, args=(1,))
        self.timer_time = 0
        self.temperature = 0
        self.menu_index = 0
        self.menu_images=[BREAD_IMAGE,ZOPF_IMAGE,BANANE_IMAGE]
        
    def state_machine(self,device,type_,value):
        if self.application_state == Application_State.Init:
            print("Init")
            self.display.init()
            self.timer.set_update_callback(self.display.show_timer_screen)
            if device == 'encoder_1' and type_ == 'position':
                self.application_state = Application_State.Menu_Dialog
                self.display.show_menu_screen(self.menu_images[0])
            elif device == 'encoder_1' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Timer_Setting
                self.display.show_timer_screen(self.timer_time)
            elif device == 'encoder_2' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Temperature_Setting
                self.display.show_temperature_screen(self.temperature)
                
        elif self.application_state == Application_State.Menu_Dialog:
            print("Menu_Dialog")
            if device == 'encoder_1' and type_ == 'position':
                if self.menu_index > 0 or value > 0:
                    self.menu_index += value
                    self.display.show_menu_screen(self.menu_images[abs(self.menu_index)%3])
            elif device == 'encoder_1' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Timer_Setting
                self.display.show_timer_screen(self.timer_time)
            elif device == 'encoder_2' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Temperature_Setting
                print("elif")
                self.display.show_temperature_screen(self.temperature)
                
                
        elif self.application_state == Application_State.Timer_Setting:
            print("Timer_Setting")
            if device == 'encoder_1' and type_ == 'position':
                if self.timer_time > 0 or value > 0:
                    self.timer_time += (value * 5)
                    self.display.show_timer_screen(self.timer_time)
            elif device == 'encoder_1' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Timer_Countdown 
                self.timer.set_remaining_time_s(self.timer_time)
                self.timer.start()
            elif device == 'encoder_2' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Temperature_Setting
                self.display.show_temperature_screen(self.temperature)

        elif self.application_state == Application_State.Temperature_Setting:
            print("temperature setting")
            if device == 'encoder_2' and type_ == 'position':
                if self.temperature > 0 or value > 0:
                    self.temperature += (value * 5)
                    self.display.show_temperature_screen(self.temperature)
            elif device == 'encoder_2' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Menu_Dialog
                self.display.show_menu_screen(self.menu_images[0])
            elif device == 'encoder_1' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Timer_Setting
                self.display.show_timer_screen(self.timer_time)

                
        elif self.application_state == Application_State.Timer_Countdown:
            print("Timer_Countdown")
            if device == 'encoder_1' and type_ == 'switch' and value == 1:
                self.application_state = Application_State.Menu_Dialog
                self.timer_time = 0
                self.timer.stop()
            
    
    def handle_peripherals(self):
        try:
            message_encoder_1 = self.encoder_1_queue.get()
            device = message_encoder_1['device']
            type_ = message_encoder_1['type']
            value = message_encoder_1['value']
            print(device)
            print(type_)
            print(value)
            self.state_machine(device,type_,value)
            self.encoder_1_queue.task_done()
            
        except:
            print("empty")
            
    def init(self):
        self.encoder_1_thread.start()
        self.encoder_2_thread.start()
        self.heater_thread.start()
        self.my_own_thread.start()
        
    def run(self,name):
        while True:
            print("hello")
            self.handle_peripherals()
            
        