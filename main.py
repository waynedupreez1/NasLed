'''
Main script for LED Control 
'''

import http_server
import led_control
import log
import logging
import sys

def setupLogger():

    global mod_logger
    mod_logger = logging.getLogger("led control")
    log.main(mod_logger, syslogging = False)
    mod_logger.info("Starting LED control code")
    http_server.loggerSetup()
    led_control.loggerSetup()

def initLEDSetup():
    led_control.stripSetup()    
    led_control.setColor('FF0000')

def main():
    #try opening a server on specified socket and keep it open
    try:
        setupLogger()
        initLEDSetup()
        tcp_server = http_server.createServer() 
        http_server.openServer(tcp_server) 
    except KeyboardInterrupt:
        http_server.closeServer(tcp_server)    
#    except Exception:    
#        pass 

# Main program logic follows:
if __name__ == '__main__':
    main()
    sys.exit(0)