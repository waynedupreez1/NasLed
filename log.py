""" 
Wayne du Preez, Glidepath Ltd
1/11/2019

Setup logger to log to rsyslog and terminal

Added:
1. Selection of LOG FACILTY and if we want syslogging
"""
import logging
import logging.handlers
import sys

#Global variables

def __setup(mod_logger, syslogging = False, facility = "LOG_LOCAL0"):	
	"""
	Private: This is not to be called from outside the module.

	This setup the spacing ect of how the debug logging structure would look like
	"""

	mod_logger.setLevel(logging.INFO)

	#Setup syslog
	if (syslogging):	
		print("here1")

		if(facility == "LOG_LOCAL0"):
			facility = logging.handlers.SysLogHandler.LOG_LOCAL0
		elif(facility == "LOG_LOCAL1"):
			facility = logging.handlers.SysLogHandler.LOG_LOCAL1
		elif(facility == "LOG_LOCAL2"):
			facility = logging.handlers.SysLogHandler.LOG_LOCAL2
		else:
			raise("Only Log facilities LOG_LOCAL0,LOG_LOCAL1,LOG_LOCAL2 defined")
			sys.exit(1)

		syslog_hdlr = logging.handlers.SysLogHandler(address="/dev/log",facility=facility)
		syslog_hdlr.setLevel(logging.INFO)
		syslog_hdlr_formatter = logging.Formatter("[%(levelname)-6s] [%(name)-20s] [%(message)s]")
		syslog_hdlr.setFormatter(syslog_hdlr_formatter)

		#Add the handlers to root logger
		mod_logger.addHandler(syslog_hdlr)
	
	#Setup console
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console_formatter = logging.Formatter("%(asctime)s [%(levelname)-6s] [%(name)-20s] [%(message)s]")
	console.setFormatter(console_formatter)
	
	#Add the handlers to root logger
	mod_logger.addHandler(console)


def main(mod_logger, syslogging = False, facility = "LOG_LOCAL0"):	

	__setup(mod_logger, syslogging = False, facility = "LOG_LOCAL0")	

if __name__ == "__main__":
	
	mod_logger = logging.getLogger(__name__)

	main(mod_logger, syslogging = True, facility = "LOG_LOCAL0")

	mod_logger.info("Log succesfull")

	sys.exit(0)	