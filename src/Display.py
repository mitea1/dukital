# -*- coding: utf-8 -*-
from Adafruit_SSD1306.SSD1306 import *
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont


TIMER_FONT = '../assets/fonts/SF Electrotome.ttf'
class Display(object):
    RST=24
    
    def __init__(self):
        self.ssd1306 = SSD1306_128_64(rst=self.RST)
        self.timer_font = ImageFont.truetype(TIMER_FONT,size=45)

        
    def init(self):
        # Initialize library.
        self.ssd1306.begin()  
        # Clear display.
        self.ssd1306.clear()
        self.ssd1306.display()
    
    def show_timer_screen(self,time):
        minutes = 0
        seconds = 0
        
        if time > 59:
            minutes = int(time/60)
            seconds = time - (minutes * 60)
            
            if minutes > 9:
                minutes_text = str(minutes)
            else:
                minutes_text = str(0)+str(minutes)
            
            if seconds > 9:
                seconds_text = str(seconds)
            else:
                seconds_text = str(0)+str(seconds)
        else:
            seconds = time
            minutes_text = "00"
            if seconds > 9:
                seconds_text = str(seconds)
            else:
                seconds_text = str(0)+str(seconds)
            
        self.timer_image = Image.new('1', (self.ssd1306.width, self.ssd1306.height),)
        self.timer_draw = ImageDraw.Draw(self.timer_image)
        self.timer_draw.text((2, -2), minutes_text+":"+seconds_text,font=self.timer_font, fill=255)
        self.ssd1306.image(self.timer_image)
        self.ssd1306.display()
        print("show_timer_screen")
    
        
        