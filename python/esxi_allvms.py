#!/usr/bin/env python
##
## Info:		A simple script to connect to ESXi host 
##			or vSphere cluster and get information
##                      about a vm
## Created by: 		Denise Medema
## Date Created: 	Nov 4 2018
## Last Updated: 
## Version:		0.1
## Changelog:		
##

import argparse
import logging
import ssl
import getpass

from pyVmomi import vim
from pyVim import connect

def getArgs():
    parser = argparse.ArgumentParser(description='Enter Arguments to Connect to vSphere')
    ## YOU WILL GET AN ERROR IF YOU COMMENT THE LINE BELOW
    ## THIS IS BUILT INTO THE ARGPARSE MODULE AND IS THERE BY DEFAULT
    #parser.add_argument('-h', '--help', action='store_true', help='Display help')
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")
    # NOTE: Adding additional variables, don't use the action= option
    #parser.add_argument('-u', '--user', help="Username to connect with", required=True)
    #parser.add_argument('-p', '--password', required=True, help="Password to connect with")
    parser.add_argument('-host', '--host', required=True, help="Enter the IP of the ESXi host or vShpere cluster")
    #parser.add_argument('-port', '--port', required=True, help="Enter port to connect on")

    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args

    #service_instance = connect.SmartConnectNoSSL(host=args.host,
    #                          user=args.user,
    #                          pwd=args.password,
    #                          port=int(args.port))
    
    #logger.debug(service_instance)

    #sslContext = localSslFixup(host, sslContext)


# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
            obj.update({managed_object_ref: managed_object_ref.name})
    return obj

def main():
    logger=logging.getLogger('esxi_connect.py')
    args = getArgs()
    logger.debug(args)

    #password= getpass.getpass('Enter the vSphere password to proceed: ')
    password='lrtLRT12$'
    user='administrator@vsphere.local'

    my_cluster = connect.ConnectNoSSL(args.host, "443", user, password)
    content=my_cluster.content
    logger.debug(content)

    #Calling above method
    getAllVms=get_all_objs(content, [vim.VirtualMachine])

    #Iterating each vm object and printing its name
    for vm in getAllVms:
        #print vm.config.uuid
        #print("%s %d %s %s" % (name, ts, val, tag_str))
        print("VM Name: %s " "VM IP Address: %s " % (vm.config.name, vm.guest.ipAddress))

if __name__ == "__main__":
    main()

