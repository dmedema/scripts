#!/usr/bin/env python
##
## Info:                This is a script to check if services need restart  
##                      after a system update and restart them
## Created by:          Denise Medema
## Date Created:        Feb 9, 2018
## Last Updated: 
## Version:             0.1
## Changelog:           
##

import os
import argparse
import logging
import subprocess 
import smtplib
import socket
from email.MIMEText import MIMEText

def getArgs():
    parser = argparse.ArgumentParser(description='Restart Services after Server Patching')
    ## YOU WILL GET AN ERROR IF YOU COMMENT THE LINE BELOW
    ## THIS IS BUILT INTO THE ARGPARSE MODULE AND IS THERE BY DEFAULT
    #parser.add_argument('-h', '--help', action='store_true', help='Display help')
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")

    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args

def send_email():
    logger=logging.getLogger('needs_restart.py')
    args = getArgs()
    logger.debug(args)

    hostname = socket.gethostname()

    mailfrom = "unixadmins@" + hostname
    mailto = "unixadmins@ipaymentinc.com"
  
    logger.debug("Mail from address is:  %s" % mailfrom)
    logger.debug("Mail to address is:  %s" % mailto)

    msg = MIMEText(needs_restart())
    
    msg['From'] = mailfrom
    msg['To'] = mailto
    msg['Subject'] = "Services require restart for " + hostname 
    
    s = smtplib.SMTP('ipaymentinc-com.mail.protection.outlook.com')    
    s.sendmail(mailfrom, mailto, msg.as_string())

    s.quit() 

def needs_restart():
    # The exit status of the command is rc

    ##### NOTE THIS IS JUST TO SHOW HOW TO PRINT EXIT STATUS ########
    #rc = subprocess.call("needs-restarting")
    #print ("The exit status needs-restarting: %d" % rc)
    ##### DO NOT USE THIS AS A TEST CASE AS THE EXIT STATUS FOR #####
    ##### THIS COMMAND IS ALWAYS 0 UNLESS THE -r FLAG IS PASSED #####
    

    # To store the output variable, run
    services = subprocess.Popen("needs-restarting", stdout=subprocess.PIPE)
    output,err = services.communicate()

    #An empty "sequences" (strings, lists, tuples), use the fact that empty sequences are false 
    if not output:
	message = ("No services need restarting!")
    else:
	message = ("The following services need restarting: %s " % output)

    return(message)


def main():
    logger=logging.getLogger('needs_restart.py')
    args = getArgs()
    #print args
    logger.debug(args)
  
    send_email()
    os.system('reboot')

if __name__ == "__main__":
    main()


