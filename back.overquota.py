#! /usr/bin/env python
# -*- coding: UTF8 -*-
## The above line specifies the encoding for this script
## Script to query XenServer vms that are over quota
## Written by Denise Lopez
## Date: March 12, 2013

# For getting the hostname
import socket
# For external bash commands
import subprocess

hostname = (socket.gethostname())
xe = "/usr/bin/xe"
xe_command = xe + " host-list name-label=" + hostname + " --minimal"

print "xe is: ", xe
print ("Hostname is: " + hostname)
print ("xe_command is: " + str(xe_command))
#hostuuid = subprocess.call(xe_command, shell=True)
hostuuid = subprocess.check_output("xe_command")
print ("hostuuid is: %s" % hostuuid)
~                                             
