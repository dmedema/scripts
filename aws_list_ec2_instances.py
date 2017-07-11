#!/usr/bin/env python
##
## Info:                This is a script to list AWS EC2 Instances
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
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            #This sample print will output entire Dictionary object
            print(instance)

            #This will print will output the value of the Dictionary key 'InstanceId'
            print(instance["InstanceId"])

if __name__ =='__main__':main()
