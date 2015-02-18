#!/usr/bin/python
## This script creates tenants from the command line
## Created by: Denise Lopez
## Date Created: Aug 27, 2014
##

import argparse, sys, subprocess

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
subnet2 = args.subnet2
subnet3 = args.subnet3

## print "Tenant Name is: %s" % tenantName
## print "Tenant Num is: %s" % tenantNum
## print "Tenant Description is: %s" % desc
## print "The first subnet is: %s" % subnet1
## print "The first gateway is: %s" % gw1
## print "The second subnet is: %s" % subnet2
## print "The third subnet is: %s" % subnet3

def getGateway(subnet):
 try:
  #Remove the last 4 characters from the string subnet1
  offset = (len(subnet) - 4)
  #Chop the last 4 characters off the string and append 1 
  gw1 = subnet[0:offset] + "1"
  return gw1
 except:
  return

def createTenant():
 try:
  print "keystone tenant-create --name %s --description '%s'" % (tenantName, desc)
  #keystone tenant-create --name tenantName --description desc 
 except:
  return

def getTenantId(name):
 try:
  # Find a way to get the id of the new tenant from keystone
  # and set the variable here
  tenantId = 10000000
  #tenantId = keystone tenant-get tenantName | grep id | awk '{ print $4 }' 
  return tenantId
 except:
  return

def setPrivs(name):
 try:
  # Add the admin and the portal users with admin privileges
  print "keystone user-role-add --user portal --role admin --tenant %s" % name
  #keystone user-role-add --user portal --role admin --tenant name
  print "keystone user-role-add --user admin --role admin --tenant %s" % name
  #keystone user-role-add --user admin --role admin --tenant name

  ID = getTenantId(name)

  # Disable quotas for the following settings
  print "nova quota-update --instances -1 %s" % ID
  print "nova quota-update --cores -1 %s" % ID
  print "nova quota-update --ram -1 %s" % ID
  print "nova quota-update --floating_ips -1 %s" % ID
  #nova quota-update --instances -1 ID
  #nova quota-update --cores -1 ID
  #nova quota-update --ram -1 ID
  #nova quota-update --floating_ips -1 ID
 except:
  return

def createNetwork(name, number):
 try:
  ID = getTenantId(name)
  # Create the openstack network
  print "neutron net-create net-%s --tenant-id %s --provider:network_type vlan --provider:physical_network physnet1 --provider:segmentation_id %s" % (name, ID, number)
  #neutron net-create net-name --tenant-id ID --provider:network_type vlan --provider:physical_network physnet1 --provider:segmentation_id number
 except:
  return

def createSubnet(name, subnet):
 try:
  ID = getTenantId(name)
  gateway = getGateway(subnet)
  # Create a one or several subnets associated with the network
  print "neutron subnet-create net-%s --tenant-id %s --name %s --gateway %s --dns-nameserver 10.75.32.5 --dns-nameserver 10.75.33.5 %s" % (name, ID, subnet, gateway, subnet)
  #neutron subnet-create net-name --tenant-id ID --name subnet --gateway gateway --dns-nameserver 10.75.32.5 --dns-nameserver 10.75.33.5 subnet
 except:
  return

def main():
 createTenant()
 setPrivs(tenantName)
 createNetwork(tenantName, tenantNum)
 createSubnet(tenantName, subnet1)
 createSubnet(tenantName, subnet2)
 createSubnet(tenantName, subnet3)

 print "Now make sure to update inventory!"

if __name__ == '__main__':
  main()
