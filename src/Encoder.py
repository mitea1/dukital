# -*- coding: utf-8 -*-
import gaugette.gpio
import gaugette.rotary_encoder
import gaugette.switch
import time
import math

class Encoder(object):
    
    def __init__(self,a_pin,b_pin,sw_pin,name):
        self.A_PIN = a_pin
        self.B_PIN = b_pin
        self.SW_PIN = sw_pin
        self.name = name
        self.position = 0
        self.cycles = 0
        gpio = gaugette.gpio.GPIO()
        self.encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, self.A_PIN, self.B_PIN)
        self.switch = gaugette.switch.Switch(gpio, self.SW_PIN)
        self.last_state = None
        self.last_switch_state = None
        self.last_delta = 0
        self.last_sequence = self.encoder.rotation_sequence()
        self.steps_per_cycle = 4 # arbitrary, usually equal to steps per detent
        self.remainder = self.steps_per_cycle//2
    
    def run(self,queue):
        print("Encoder run")
        while True:
        
            state = self.encoder.rotation_state()
            switch_state = self.switch.get_state()
        
            if (state != self.last_state):
                self.last_state = state
        
                # extract individual signal bits for A and B
                a_state = state & 0x01
                b_state = (state & 0x02) >> 1
        
                # compute sequence number:
                # This is the same as the value returned by encoder.rotation_sequence()
                sequence = (a_state ^ b_state) | b_state << 1
        
                # compute delta:
                # This is the same as the value returned by encoder.get_delta()
                delta = (sequence - self.last_sequence) % 4
                if delta == 3:
                    delta = -1
                elif delta==2:
                    # this is an attempt to make sense out of a missed step:
                    # assume that we have moved two steps in the same direction
                    # that we were previously moving.
                    delta = int(math.copysign(delta, self.last_delta))
                self.last_delta = delta
                self.last_sequence = sequence
        
                self.remainder += delta
                self.cycles = self.remainder // self.steps_per_cycle
                self.remainder %= self.steps_per_cycle
        

                self.position += delta
                message=dict([('device',self.name),
                              ('type','position'),
                              ('value',self.position)])
                queue.put(message)
                print(message)
            
            if (switch_state != self.last_switch_state):
                self.last_switch_state = switch_state
                if switch_state == 1:
                    message=dict([('device',self.name),
                                  ('type','switch'),
                                  ('value',switch_state)])
                    queue.put(message)
                    print(message)
                
            time.sleep(0.1)