""" 
Wayne du Preez
04/11/2020

LED Control Script
"""

import re
import time
from rpi_ws281x import PixelStrip, Color, WS2811_STRIP_BGR
import argparse
import log
import logging
import sys

# LED strip configuration:
LED_COUNT      = 50     # Number of LED pixels. Number of sections 
LED_PIN_CH_0   = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 5     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL_0  = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#set the colour as requested
def setColor(color):
    color_int = int(color,16)
    mod_logger.info("Setting Colour")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color_int)
    strip.show()

#fade to colour as requested
def fade(color, delay):
    mod_logger.info("Fading from current colour to defined colour")
    #next color
    color_int = int(color,16)
    blue = color_int & 255
    green = (color_int >> 8) & 255
    red = (color_int >> 16) & 255
    
    #current color
    current_blue = strip.getPixelColor(0) & 255
    current_green = (strip.getPixelColor(0) >>8) & 255
    current_red = (strip.getPixelColor(0)>>16) & 255
    
    n = int(delay)
    for j in range(n):
        set_red = current_red + (red-current_red)*(j+1)//n
        set_green = current_green + (green-current_green)*(j+1)//n
        set_blue = current_blue + (blue-current_blue)*(j+1)//n
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(set_red, set_green, set_blue))
        strip.show()
        time.sleep(0.001)

#spiral upwards or downwards
def spiral(color, duration, direction):
    duration_int = int(duration)//LED_COUNT
    color_int = int(color,16)
    mod_logger.info("Spiral")

    setColor("0")

    for i in range(strip.numPixels()):
        if(direction == "down"):
            strip.setPixelColor(i, color_int)
        else:
            strip.setPixelColor((strip.numPixels() - i), color_int)
        strip.show()
        time.sleep(duration_int/1000.0)

#TO DO: FIX THIS FUNCTION
#glow 
def glow(color, delay):
    color_int = int(color,16)
    mod_logger.info("Fade to colour from current colour to defined colour and glow")
    fade(color,delay)
    for i in range(125):
        strip.setBrightness(255-i)
        strip.show()
        time.sleep(0.001)
    for i in range(125):
        strip.setBrightness(125+i)
        strip.show()
        time.sleep(0.001)

def wipe(color, duration):
    duration_int = int(duration)//LED_COUNT
    color_int = int(color,16)
    mod_logger.info("Wipe across led strip")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color_int)
        strip.show()
        time.sleep(duration_int/1000.0)

        
def stripSetup():
    global strip 
    strip = PixelStrip(LED_COUNT, LED_PIN_CH_0, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_0, WS2811_STRIP_BGR)
    strip.begin()
    
    
def loggerSetup():
    global mod_logger
    mod_logger = logging.getLogger(__name__)
    log.main(mod_logger, syslogging = False)


def main(mod_logger, syslogging = False, facility = "LOG_LOCAL0"):

    stripSetup()

    while(1):
        print("FF0000")
        spiral('FF0000',5000, "up")

        print("00FF00")
        spiral('00FF00',5000, "up")

        print("0000FF")
        spiral('0000FF',5000, "up")


if __name__ == "__main__":
	
	mod_logger = logging.getLogger(__name__)

	main(mod_logger, syslogging = False, facility = "LOG_LOCAL0")

	mod_logger.info("Log succesfull")

	sys.exit(0)	