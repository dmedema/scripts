#!/usr/bin/env python
##
## Info:                This is a script to an AWS EC2 Instances
##                      Name and InstanceId
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


def get_instance_name(fid):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancenaem = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return instancename


def main():
    ec2 = boto3.client('ec2')

    # Retrieves all InstanceIds that with EC2 and print the Name Tag
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            print(instance["InstanceId"])
            name=get_instance_name(instance["InstanceId"])
            print name

if __name__ =='__main__':main()
