#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 21:42:07 2020

@author: pi
"""
from LPD8806_Python3.raspledstrip.ledstrip import*
from Adafruit_SSD1306.SSD1306 import *
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont
import threading
import time
import gaugette.platform
import gaugette.gpio
import gaugette.rotary_encoder
import gaugette.switch
import math
from queue import Queue
from Timer import Timer
from Display import Display
from Encoder import Encoder
from Application import Application


def led_control_thread(name):
    led = LEDStrip(20,True)
    led.fillRGB(0,255,255)
    led.update()
    brightness = [0.6,0.7,0.8,0.9]
    led.setMasterBrightness(0.5)
    index = 0
    while True:
        led.setMasterBrightness(brightness[index%4])
        led.update()
        index+=1
        time.sleep(0.1)
        

def rotary_encoder_thread(queue):
    A_PIN  = 21
    B_PIN  = 23
    SW_PIN = 22

    position = 0
    
    gpio = gaugette.gpio.GPIO()
    encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, A_PIN, B_PIN)
    switch = gaugette.switch.Switch(gpio, SW_PIN)
    
    last_state = None
    last_switch_state = None
    last_delta = 0
    last_sequence = encoder.rotation_sequence()
    last_heading = 0
    
    # for coarser granularity reading
    steps_per_cycle = 4 # arbitrary, usually equal to steps per detent
    remainder = steps_per_cycle//2
    
    
    # NOTE: the library includes individual calls to get
    # the rotation_state, rotation_sequence and delta values.
    # However this demo only reads the rotation_state and locally
    # derives the rotation_sequence and delta.  This ensures that
    # the derived values are based on the same two input bits A and B.
    # If we used the library calls, there is a very real chance that
    # the inputs would change while we were sampling, giving us
    # inconsistent values in the output table.
    
    while True:
    
        state = encoder.rotation_state()
        switch_state = switch.get_state()
    
        if (state != last_state or switch_state != last_switch_state):
            last_switch_state = switch_state
            last_state = state
    
            # print a heading every 20 lines
            if last_heading % 20 == 0:
              print ("A B STATE SEQ DELTA CYCLES SWITCH")
            last_heading += 1
    
            # extract individual signal bits for A and B
            a_state = state & 0x01
            b_state = (state & 0x02) >> 1
    
            # compute sequence number:
            # This is the same as the value returned by encoder.rotation_sequence()
            sequence = (a_state ^ b_state) | b_state << 1
    
            # compute delta:
            # This is the same as the value returned by encoder.get_delta()
            delta = (sequence - last_sequence) % 4
            if delta == 3:
                delta = -1
            elif delta==2:
                # this is an attempt to make sense out of a missed step:
                # assume that we have moved two steps in the same direction
                # that we were previously moving.
                delta = int(math.copysign(delta, last_delta))
            last_delta = delta
            last_sequence = sequence
    
            remainder += delta
            cycles = remainder // steps_per_cycle
            remainder %= steps_per_cycle
    
            print ('%1d %1d %3d %4d %4d %4d %4d' % (a_state, b_state, state, sequence, delta, cycles, switch_state))
            position += delta
            queue.put(position)
        time.sleep(0.1)


def display_thread(queue):
    RST = 24

    disp = SSD1306_128_64(rst=RST)
    
    
    # Initialize library.
    disp.begin()
    
    # Clear display.
    disp.clear()
    disp.display()
    
    images=[BREAD_IMAGE,BANANE_IMAGE,ZOPF_IMAGE]
    #image = Image.open('../assets/m_mais.PPM').convert('1')
    
    image = Image.open(images[0]).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    draw = ImageDraw.Draw(image)
    # Load default font.
    font = ImageFont.load_default()

    disp.image(image)
    disp.display()
    print("hello") 
    while True:
        print("queu not empty")
        position = queue.get()
        print("display position:"+str(position))
        image = Image.new('1', (disp.width, disp.height),)
        draw = ImageDraw.Draw(image)
        draw.text((2, -2),       "Position: " + str(position),  font=font, fill=255)
        disp.image(image)
        disp.display()
        queue.task_done()
        
def callback(remaining_time):
    RST = 24
    disp = SSD1306_128_64(rst=RST)
    # Initialize library.
    disp.begin()
    # Clear display.
    disp.clear()
    disp.display()
    font = ImageFont.truetype(TIMER_FONT,size=15)


    image = Image.new('1', (disp.width, disp.height),)
    draw = ImageDraw.Draw(image)
    draw.text((2, -2),       "Time: " + str(remaining_time),  font=font, fill=255)
    disp.image(image)
    disp.display()
    print("Callback demo:" + str(remaining_time))

        

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
    application = Application(display,timer,encoder_1,encoder_2)
    
    application.init()
 
