#!/usr/bin/env python
##
## Info:		This is a script to perform snmpwalk without 
##			entering the password on the command line
## Created by: 		Denise Medema
## Date Created: 	Jun 14, 2017
## Last Updated:        Jun 27, 2017 
## Version:		0.1
## Changelog:		Working to verify snmp v2 can connect
## To Do:               Modify for snmp v3
##

import argparse
import logging
import getpass
import sys

from easysnmp import Session
from easysnmp import snmp_get, snmp_walk

def getArgs():
    parser = argparse.ArgumentParser(description='Script to snmpwalk a server without entering a password on the commandline')
    ## YOU WILL GET AN ERROR IF YOU COMMENT THE LINE BELOW
    ## THIS IS BUILT INTO THE ARGPARSE MODULE AND IS THERE BY DEFAULT
    #parser.add_argument('-h', '--help', action='store_true', help='Display help')
    parser.add_argument('-host', '--hostname',  help="Enter the hostname you want to query", required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")

    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args

def main():
    logger=logging.getLogger('snmpwalk_v3.py')
    args = getArgs()
    #print args
    logger.debug("The hostname is: %s " % ( args.hostname ))
    HOST=args.hostname

    print "Please Auth Pass: "
    authPass=getpass.getpass()
    #print ("The auth password you entered was: %s " % authPass)

    print "Please enter Priv Pass: "
    privPass=getpass.getpass()
    #print ("The priv password you entered was: %s " % privPass)

    session = Session(hostname=HOST, security_level='auth_with_privacy', security_username='sa_linux_snmp_v3', privacy_protocol='AES', privacy_password=privPass, auth_protocol='SHA', auth_password=authPass, version=3)


    logger.debug("The Session info is: %s " % session)

    location = session.get('sysDescr.0')

    print("The Location of this system is: %s " % location)
    logger.debug(args)


if __name__ == "__main__":
    main()

