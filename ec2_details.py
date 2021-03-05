#!/usr/bin/env python3 
import os
import sys
import boto3
import datetime

total = len(sys.argv)
cmdargs = str(sys.argv)

if total < 3 or total > 3:
    print('Usage {} <customer profile> <region>'.format(sys.argv[0]))
    exit(1)


customer=str(sys.argv[1])
region=str(sys.argv[2])
session = boto3.Session(profile_name=customer,region_name=region)
#ec2 = session.client('ec2')

#response = ec2.describe_instances()

#for r in response['Reservations']:
#    for i in r['Instances']:
#       print(i['Tags'])
#        for tag in i.tags:
#            print('Found instance id: ' + instance.id + '\ntag: ' + tag)

ec2 = session.resource('ec2')
once=0
tag_keys= {"Instance_ID"}
tag_values = {}
display_format={"Name","Instance_Type","Availablity_Zone","Instance_State","Launch_Time","Security_Groups","VPC_ID","Subnet_ID","Elastic_IP","Private_IP","Volumes"}

for i in ec2.instances.all():
    tag_str={}
    tag_keys.add("Name")
    tag_str["Instance_ID"]=i.instance_id
    tag_keys.add("Name")
    for tag in i.tags:
       if tag['Key'] == "Name":
           tag_str["Name"]=tag['Value']
    tag_keys.add("Instance_State")
    tag_str["Instance_State"]=i.state['Name']
    tag_keys.add("Private_IP")
    tag_str["Private_IP"]=i.private_ip_address
    tag_keys.add("Elastic_IP")
    if i.public_ip_address:
        tag_str["Elastic_IP"]=i.public_ip_address
    else:
        tag_str["Elastic_IP"]=""
    tag_keys.add("Instance_Type")
    tag_str["Instance_Type"]=i.instance_type
    tag_keys.add("Availablity_Zone")
    tag_str["Availablity_Zone"]=i.placement['AvailabilityZone']
    tag_keys.add("Launch_Time")
    tag_str["Launch_Time"]=i.launch_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    tag_keys.add("VPC_ID")
    tag_str["VPC_ID"]=i.vpc_id
    tag_keys.add("Subnet_ID")
    tag_str["Subnet_ID"]=i.subnet_id
    vid="Volumes(id size type)"
    tag_keys.add("Volumes")
    vol_str=""
    for v in i.volumes.all():
        vol_str=vol_str+str(v.id)+" "+str(v.size)+" GiB "+str(v.volume_type)+"\n" 
    tag_str["Volumes"]=vol_str
    tag_keys.add("Security_Groups")
    sg_str=""
    for sg in i.security_groups:
        sg_str=sg_str+sg['GroupName']+"\n"
    tag_str["Security_Groups"]=sg_str
    tag_values[i.instance_id]=tag_str
key_str="Instance_ID"
for i in display_format:
        key_str=key_str+','+ i
print(key_str)


#print(tag_values.keys())

for i,tags in tag_values.items():
    value_str="\""+i+"\","
#    print(tags)
    for j in display_format:
          value_str=value_str+"\""+tags[j]+"\","
    print(value_str)
