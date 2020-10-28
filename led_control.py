'''
Script that changes strip animation based on request

Adeshwar Gounder 


'''

import re
import time
from rpi_ws281x import PixelStrip, Color
import argparse
import log
import logging
import threading

# LED strip configuration:
LED_COUNT      = 70      # Number of LED pixels. Number of sections 
LED_PIN_CH_0   = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN_CH_1   = 19
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 11      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL_0  = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_CHANNEL_1  = 1

#set the colour as requested
def setColor(color):
    color_int = int(color,16)
    mod_logger.info("Setting Colour")
    for i in range(front_strip.numPixels()):
        front_strip.setPixelColor(i, color_int)
        wall_strip.setPixelColor(i, color_int)
    front_strip.show()
    wall_strip.show()


#fade to colour as requested
def fade(color, delay):
    mod_logger.info("Fading from current colour to defined colour")
    #next color
    color_int = int(color,16)
    blue = color_int & 255
    green = (color_int >> 8) & 255
    red = (color_int >> 16) & 255
    
    #current color
    current_blue = front_strip.getPixelColor(0) & 255
    current_green = (front_strip.getPixelColor(0) >>8) & 255
    current_red = (front_strip.getPixelColor(0)>>16) & 255
    
    n = int(delay)
    for j in range(n):
        set_red = current_red + (red-current_red)*(j+1)//n
        set_green = current_green + (green-current_green)*(j+1)//n
        set_blue = current_blue + (blue-current_blue)*(j+1)//n
        for i in range(front_strip.numPixels()):
            front_strip.setPixelColor(i, Color(set_red, set_green, set_blue))
            wall_strip.setPixelColor(i, Color(set_red, set_green, set_blue))
        front_strip.show()
        wall_strip.show()
        time.sleep(0.001)



#TO DO: FIX THIS FUNCTION
#glow 
def glow(color, delay):
    color_int = int(color,16)
    mod_logger.info("Fade to colour from current colour to defined colour and glow")
    fade(color,delay)
    for i in range(125):
        front_strip.setBrightness(255-i)
        front_strip.show()
        time.sleep(0.01)
    for i in range(125):
        front_strip.setBrightness(125+i)
        front_strip.show()
        time.sleep(0.01)

def wipe(color, duration):
    duration_int = int(duration)//LED_COUNT
    color_int = int(color,16)
    mod_logger.info("Wipe across led strip")
    for i in range(front_strip.numPixels()):
        front_strip.setPixelColor(i, color_int)
        wall_strip.setPixelColor(i, color_int)
        front_strip.show()
        wall_strip.show()
        time.sleep(duration_int/1000.0)
        
#TO DO: Keyboard interrupt break from thread
def test_mode_animation():
    while(test_mode):
        for i in range(front_strip.numPixels()):
            front_strip.setPixelColor(i, Color(255,0,0))
            wall_strip.setPixelColor(i, Color(255,0,0))
        front_strip.show()
        wall_strip.show()
        time.sleep(1)
        for i in range(front_strip.numPixels()):
            front_strip.setPixelColor(i, Color(0,255,0))
            wall_strip.setPixelColor(i, Color(0,255,0))
        front_strip.show()
        wall_strip.show()
        time.sleep(1)
        for i in range(front_strip.numPixels()):
            front_strip.setPixelColor(i, Color(0,0,255))
            wall_strip.setPixelColor(i, Color(0,0,255))
        front_strip.show()
        wall_strip.show()
        time.sleep(1)
    for i in range(front_strip.numPixels()):
        front_strip.setPixelColor(i, Color(255,255,255))
        wall_strip.setPixelColor(i, Color(255,255,255))
    front_strip.show()
    wall_strip.show()


#change mode as requested
def setMode(mode):
    global test_mode
    if mode == '0':
        test_mode = False
    elif mode == '1':
        test_mode = True
        thread = threading.Thread(target=test_mode_animation)
        thread.start()
        
def stripSetup():
    global front_strip
    global wall_strip   
    front_strip = PixelStrip(LED_COUNT, LED_PIN_CH_0, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_0)
    wall_strip = PixelStrip(LED_COUNT, LED_PIN_CH_1, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_1)
    front_strip.begin()
    wall_strip.begin()
    
    
def loggerSetup():
    global mod_logger
    mod_logger = logging.getLogger(__name__)
    log.main(mod_logger, syslogging = True)
