'''
Script that opens a http server on default port 80

Adeshwar Gounder 

HOSTNAME - ip address to create server on, most likely it will be 10.0.0.32
PORT - port to create server on, http default is 80, https default is 443. 

'''

import socketserver
from http import server
import re
##import led_control
##from furl import furl
import logging
import log

#OSTNAME = "0.0.0.0"
#PORT = 80

HOSTNAME = "127.0.0.1"
PORT = 8080

#Handler class describes what to do with response
class requestHandler(server.SimpleHTTPRequestHandler): 
    def do_GET(self):

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        if self.path == '/':
            self.path = 'index.html'
        return server.SimpleHTTPRequestHandler.do_GET(self)


"""         try:
            mod_logger.info("Handling Request")
            f = furl(self.path)
            if f.args['action'] == 'set_mode':
                led_control.setMode(f.args['op_mode'])
            elif f.args['action'] == 'fade':
                led_control.fade(f.args['color'], f.args['duration'])    
            elif f.args['action'] == 'glow':
                led_control.glow(f.args['color'], f.args['duration'])   
            elif f.args['action'] == 'wipe':
                led_control.wipe(f.args['color'], f.args['duration'])   
            elif f.args['action'] == 'set':
                led_control.setColor(f.args['color'])
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            #mod_logger.info("Header Sent")
            self.send_header('Content-type', 'text/html')
            self.send_response(200) #OK Status response       
            #self.send_header('Content-type', 'text/html')
            self.end_headers()
            mod_logger.info("Response Sent")     
        except Exception:
            self.send_response(400) """

def createServer():
    mod_logger.info("Creating Server on : %s Port: %d",HOSTNAME ,PORT)
    tcp_server = socketserver.TCPServer((HOSTNAME, PORT), requestHandler)
    return tcp_server
#try opening a server on specified socket and keep it open
def openServer(tcp_server):
    mod_logger.info("Opening Server")
    tcp_server.serve_forever()
    

#close server
def closeServer(tcp_server):
    mod_logger.info("Closing Server")
    tcp_server.socket.close()
    
def loggerSetup():
    global mod_logger
    mod_logger = logging.getLogger(__name__)
    log.main(mod_logger, syslogging = True)


def main(mod_logger, syslogging = False, facility = "LOG_LOCAL0"):

    try:
        tcp_server = createServer() 
        openServer(tcp_server) 
    except KeyboardInterrupt:
        closeServer(tcp_server)  


if __name__ == "__main__":
	
	mod_logger = logging.getLogger(__name__)

	main(mod_logger, syslogging = False, facility = "LOG_LOCAL0")

	mod_logger.info("Log succesfull")

	sys.exit(0)	
