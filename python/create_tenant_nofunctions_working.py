#!/usr/bin/python
## This script creates tenants from the command line
## Created by: Denise Lopez
## Date Created: Aug 27, 2014
##

import argparse, sys

parser = argparse.ArgumentParser(description='This is a create tenant for openstack')

parser.add_argument('--tenantName', required=True, action="store")
parser.add_argument('--desc', required=True, action="store")
parser.add_argument('--subnet1', required=True, action="store")
parser.add_argument('--subnet2', action="store")
parser.add_argument('--subnet3', action="store")

args = parser.parse_args()
##print parser.parse_args() 

tenantName = args.tenantName
#Remove the t from the tenantName
tenantNum = tenantName[1:] 
desc = args.desc
subnet1 = args.subnet1
#Remove the last 4 characters from the string subnet1
offset1 = (len(subnet1) - 4)
#Chop the last 4 characters off the string and append 1 
gw1 = subnet1[0:offset1] + "1"
subnet2 = args.subnet2
subnet3 = args.subnet3

## print "Tenant Name is: %s" % tenantName
## print "Tenant Num is: %s" % tenantNum
## print "Tenant Description is: %s" % desc
## print "The first subnet is: %s" % subnet1
## print "The first gateway is: %s" % gw1
## print "The second subnet is: %s" % subnet2
## print "The third subnet is: %s" % subnet3

# Create the tenant
print "keystone tenant-create --name %s --description '%s'" % (tenantName, desc)
#keystone tenant-create --name tenantName --description desc 

# Find a way to get the id of the new tenant from keystone
# and set the variable here
tenantId = 10000000
#tenantId = keystone tenant-get tenantName | grep id | awk '{ print $4 }' 

# Add the admin and the portal users with admin privileges
print "keystone user-role-add --user admin --role admin --tenant %s" % tenantName
#keystone user-role-add --user portal --role admin --tenant tenantName

# Disable quotas for the following settings
print "nova quota-update --instances -1 %s" % tenantId
print "nova quota-update --cores -1 %s" % tenantId
print "nova quota-update --ram -1 %s" %tenantId
print "nova quota-update --floating_ips -1 %s" % tenantId
#nova quota-update --instances -1 tenantId
#nova quota-update --cores -1 tenantId
#nova quota-update --ram -1 tenantId
#nova quota-update --floating_ips -1 tenantId

# Create the openstack network
print "neutron net-create net-%s --tenant-id %s --provider:network_type vlan --provider:physical_network physnet1 --provider:segmentation_id %s" % (tenantNum, tenantId, tenantNum)
#neutron net-create net-tenantNum --tenant-id tenantId --provider:network_type vlan --provider:physical_network physnet1 --provider:segmentation_id tenantNum

# Create a one or several subnets associated with the network
# This should get extended to a for loop to go through the subnets given on the command line
print "neutron subnet-create net-%s --tenant-id %s --name %s --gateway 10.73.240.1 --dns-nameserver 10.75.32.5 --dns-nameserver 10.75.33.5 %s" % (tenantNum, tenantId, subnet1, subnet1)
#neutron subnet-create net-tenantNum --tenant-id tenantId --name subnet1 --gateway 10.73.240.1 --dns-nameserver 10.75.32.5 --dns-nameserver 10.75.33.5 subnet1

print "Now make sure to update inventory!"

