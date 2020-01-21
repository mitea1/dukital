# -*- coding: utf-8 -*-
from Adafruit_SSD1306.SSD1306 import *
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont


TIMER_FONT = '../assets/fonts/SF Electrotome.ttf'
TEMPERATURE_FONT = TIMER_FONT

class Display(object):
    RST=24
    
    def __init__(self):
        self.ssd1306 = SSD1306_128_64(rst=self.RST)
        self.timer_font = ImageFont.truetype(TIMER_FONT,size=45)
        self.temperature_font = ImageFont.truetype(TEMPERATURE_FONT,size=45)

        
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
        
        
    def show_temperature_screen(self, temperature):
        self.temperature_image = Image.new('1', (self.ssd1306.width, self.ssd1306.height),)
        self.temperature_draw = ImageDraw.Draw(self.temperature_image)
        
        if temperature >= 100:
            third_digit = int(temperature/100)
            second_digit = int((temperature-(third_digit * 100))/10)
            first_digit = temperature - (second_digit * 10) - (third_digit * 100)
            self.temperature_draw.text((2 + 20, -2), str(third_digit),font=self.temperature_font, fill=255)
            self.temperature_draw.text((2 + 2*20, -2), str(second_digit),font=self.temperature_font, fill=255)
        elif temperature >= 10:
            second_digit = int(temperature/10)
            first_digit = temperature - (second_digit * 10)
            self.temperature_draw.text((2 + 2*20, -2), str(second_digit),font=self.temperature_font, fill=255)
        else:
            first_digit = temperature
            
        self.temperature_draw.text((2 + 3*20, -2), str(first_digit),font=self.temperature_font, fill=255)    
        self.temperature_draw.text((2 + 4*20, -2),"°C",font=self.temperature_font, fill=255)
        self.ssd1306.image(self.temperature_image)
        self.ssd1306.display()
        print("show_temperature_screen")
        
    def show_menu_screen(self,menu_image):
        image = Image.open(menu_image).resize((self.ssd1306.width, self.ssd1306.height), Image.ANTIALIAS).convert('1')
        self.ssd1306.image(image)
        self.ssd1306.display()
    
        
        