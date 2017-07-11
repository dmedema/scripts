#!/usr/bin/env python
##
## Info:                This is a script to list AWS EC2 Regions
##                      and Availability Zones
##                      
## Created by:          Denise Medema
## Date Created:        Jul 11, 2017
## Last Updated: 
## Version:             0.1
## Changelog:           
##
##
##
##
##

import argparse
import boto3


def main():
    ec2 = boto3.client('ec2')

    # Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_regions()
    print('Regions:', response['Regions'])

    #Retrieves availablity zones only for region of the ec2 object
    response = ec2.describe_availability_zones()
    print('Availability Zones:', response['AvailabilityZones'])

if __name__ =='__main__':main()
