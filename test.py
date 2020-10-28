'''
Script that opens a http server on default port 80

Adeshwar Gounder 

HOSTNAME - ip address to create server on, most likely it will be 10.0.0.32
PORT - port to create server on, http default is 80, https default is 443. 

'''
import logging
import log
import requests
import main
import threading
import time
def start_server():
    main.main()


def loggerSetup():
    global mod_logger
    mod_logger = logging.getLogger("led function test")
    log.main(mod_logger, syslogging = True)

# Main program logic follows:
if __name__ == '__main__':
    loggerSetup()
    
    mod_logger.info("Starting Server")
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    time.sleep(5)
    try:    
        while True:
            
            mod_logger.info("Test - Set_Colour Function")
            response = requests.get('http://127.0.0.1/?action=set&color=00FF00')

            time.sleep(2)
    
            mod_logger.info("Test - Fade Function")
            response = requests.get('http://127.0.0.1/?action=fade&color=0000FF&duration=250')
    
            time.sleep(3)
    
            mod_logger.info("Test - Wipe Function")
            response = requests.get('http://127.0.0.1/?action=wipe&color=FF0000&duration=4000')
    
            time.sleep(5)
    
            mod_logger.info("Test - Set_Mode Function")
            response = requests.get('http://127.0.0.1/?action=set_mode&op_mode=1')
    
            time.sleep(10)
    
            mod_logger.info("Set to production mode")
            response = requests.get('http://127.0.0.1/?action=set_mode&op_mode=0')
    
            time.sleep(5)
    except KeyboardInterrupt: 
        mod_logger.info("Tests finshed, Closing Server")
