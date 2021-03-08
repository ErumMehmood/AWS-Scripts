'''
-----------------------------------------------------------------
How to Run: create_tags.py default us-east-1 Key1:Value1 Key2:Value2
-----------------------------------------------------------------
'''
#####################################################################################
#!/usr/bin/env python3 
import os
import sys
import boto3
import datetime
import xlrd
import csv


total = len(sys.argv)
cmdargs = str(sys.argv)


if total < 4:
    print('Usage {} <customer profile> <region> <tags filename>'.format(sys.argv[0]))
    exit(1)


customer=str(sys.argv[1])
region=str(sys.argv[2])
tags_file = (sys.argv[3:])
tag_keys = []
tag_values = []
for each in tags_file:
    tag = each.split(':')
    tag_keys.append(tag[0])
    tag_values.append(tag[1])
session = boto3.Session(profile_name=customer,region_name=region)
ec2 = session.resource('ec2')

for i in ec2.instances.all():
    #print(i.tags)
    tags_list = i.tags
    for j in range(len(tag_keys)):
        #print(new_tag, value)
        response = ec2.create_tags(
            DryRun=False,
            Resources= [i.id,],
            Tags=[{'Key': tag_keys[j], 'Value': tag_values[j]}])
                   
