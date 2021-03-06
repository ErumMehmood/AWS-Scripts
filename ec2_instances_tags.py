
'''
Script to get instance ids and tags for servers based on following conditions:
condition 1: First find if instance name tag list excel file(instances_names.xlsx)
            is available then, get all instance ids and tags for those servers
condition 2:  otherwise get all instance ids and tags for all servers
---------------------------------------------------------------------------
How to Run: ec2_instances_tags.py default us-east-1 instances_names.xlsx
                OR
            ec2_instances_tags.py default us-east-1
---------------------------------------------------------------------------
'''

#!/usr/bin/env python3 
import os
import sys
import boto3
import datetime
import xlrd
import csv

    
#-------------------------------------------------
total = len(sys.argv)
cmdargs = str(sys.argv)


if total < 3 or total > 4:
    print('Usage {} <customer profile> <region>'.format(sys.argv[0]))
    exit(1)


customer=str(sys.argv[1])
region=str(sys.argv[2])
session = boto3.Session(profile_name=customer,region_name=region)
ec2 = session.resource('ec2')

fieldnames = ['Name','Instance ID']
with open('Names_InstanceIDs_Output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # checks if any instance_names file exists
    # by checking 4th command line argument
    if total == 4:    
        # Give the location of file
        loc = sys.argv[3]
        try:
            # To open Workbook
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            num_cols = sheet.ncols   # Number of columns
            # Iterate through rows starting from 1st row
            for row_idx in range(0, sheet.nrows):
                # for tag in Column A
                tag_search = (sheet.cell_value(row_idx,0))
                #print(tag_search)
                for i in ec2.instances.all():
                    for tag in i.tags:
                       # matches tag_search with ec2-tag 
                       if tag['Value'] == tag_search:
                           instance_name = tag['Value']
                           #print(instance_name, i.id)
                           writer.writerow({'Name': instance_name, 'Instance ID':i.id})
        except:
            print("File doesnt exist or wrong filename/path")
    else:
        #create backup for all instances
        for i in ec2.instances.all():
            for tag in i.tags:
               if tag['Key'] == "Name":
                   instance_name = tag['Value']
            #print(instance_name, i.id)
            writer.writerow({'Name': instance_name, 'Instance ID':i.id})

