#!/usr/bin/env python
##
## Info:		This is a skeleton python script with just 
##			argparse and main
## Created by: 		Denise Medema
## Date Created: 	Jul 6, 2015
## Last Updated: 
## Version:		0.1
## Changelog:		
##
##
##
##
##

import argparse
import logging

def getArgs():
    parser = argparse.ArgumentParser(description='Enter Description Here')
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

def main():
    logger=logging.getLogger('skeleton.py')
    args = getArgs()
    #print args
    logger.debug(args)


if __name__ == "__main__":
    main()

