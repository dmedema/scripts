#!/usr/bin/env python
##
## Info:		This is a script to convert html files in a directory
##                      to PDF files
## Created by: 		Denise Medema
## Date Created: 	Jul 26, 2017
## Last Updated: 
## Version:		0.1
## Changelog:		
##
##
## NOTES: This script is written to take a list of files in a directory
## and convert them from HTML to PDF
##
## ToDo: Need to add error checking on directory argument

import argparse
import logging
import pdfkit
import os

def getArgs():
    parser = argparse.ArgumentParser(description='This is a script to convert HTML files to PDF')
    ## YOU WILL GET AN ERROR IF YOU COMMENT THE LINE BELOW
    ## THIS IS BUILT INTO THE ARGPARSE MODULE AND IS THERE BY DEFAULT
    #parser.add_argument('-h', '--help', action='store_true', help='Display help')
    parser.add_argument('directory',help='Enter the directory where files are stored',action='store')

    #parser.add_argument('-d', '--directory', action='store_true', help="Enter the directory where the HTML files reside", required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")

    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args

def convertToPdf(fileName):
    logger=logging.getLogger('htmltopdf.py')

    logger.debug(fileName)

    splitfileName=fileName.split(".")
    logger.debug(splitfileName)
    logger.debug(splitfileName[0])

    outfileName=splitfileName[0] + ".pdf"
    logger.debug(outfileName)

    # Call the function with a HTML file
    print fileName
    #pdfkit.from_file(fileName , outfileName)
    

def main():
    logger=logging.getLogger('htmltopdf.py')
    args = getArgs()
    logger.debug(args)
    #logger.debug(args.directory)
    directory=args.directory

    #Get a list of html files in the current directory.
    fileList = os.listdir(directory)
    print fileList
    for x in fileList:
        convertToPdf(x)

if __name__ == "__main__":
    main()

