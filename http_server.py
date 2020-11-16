'''
Script that opens a http server on default port 80

Adeshwar Gounder 

HOSTNAME - ip address to create server on, most likely it will be 10.0.0.32
PORT - port to create server on, http default is 80, https default is 443. 

'''

import socketserver
from http import server
import re
import led_control
from furl import furl
import logging
import log
import sys

HOSTNAME = "0.0.0.0"
PORT = 80

#Handler class describes what to do with response
class requestHandler(server.SimpleHTTPRequestHandler): 
    def do_GET(self):

        mod_logger.info("Handling Request")

        try:
            f = furl(self.path)

            if len(f.args) > 0:          
                if f.args["action"] == "set":
                    led_control.setColor(f.args["color"])
                #elif f.args['action'] == 'fade':
                #    led_control.fade(f.args['color'], f.args['duration'])    
                #elif f.args['action'] == 'glow':
                #    led_control.glow(f.args['color'], f.args['duration'])   
                #elif f.args['action'] == 'wipe':
                #    led_control.wipe(f.args['color'], f.args['duration'])

            mod_logger.info("Response Sent") 

            # Sending an '200 OK' response
            self.send_response(200)

            # Setting the header
            self.send_header("Content-type", "text/html")

            # Whenever using 'send_header', you also have to call 'end_headers'
            self.end_headers()

            self.path = "index.html"
            return server.SimpleHTTPRequestHandler.do_GET(self)
        except Exception:
            mod_logger.info("Response Failed With Error")
            self.send_response(400)

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
    log.main(mod_logger, syslogging = False)


def main():

    try:
        tcp_server = createServer() 
        openServer(tcp_server) 
    except KeyboardInterrupt:
        closeServer(tcp_server)  


if __name__ == "__main__":

    loggerSetup()
    main()
    sys.exit(0)