#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import boto.ec2
import sys
import os
import fnmatch
import argparse
import subprocess
import random
import time


key_directory = 'change_this_to_point_to_folder_where_your_ssh_keys_are_stored'
ssh_commands_list = []
regions = ['us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1','ap-southeast-1','ap-southeast-2','ap-northeast-1']

### add more credentials here
credentials = {

	'dev' : { "aws_access_key_id" : "XXX", "aws_secret_access_key" :"XXXX" },
 	'prod' : { "aws_access_key_id" : "XXX", "aws_secret_access_key" :"XXXXX" },
 	'stage' : { "aws_access_key_id" : "XXX", "aws_secret_access_key" :"XXXXXX" }
}

def search_files(file_name,search_directory):
	matches = []
	for root, dirnames, filenames in os.walk(search_directory):
  		for filename in fnmatch.filter(filenames, file_name):
			matches.append(os.path.join(root, filename))
	return matches

def search_instances(instance_name='backstage',account_name='prod'):
	for aws_region in regions:
		conn =  boto.ec2.connect_to_region(aws_region,aws_access_key_id=credentials[account_name]['aws_access_key_id'],aws_secret_access_key=credentials[account_name]['aws_secret_access_key'])
		reservations = conn.get_all_instances()
		ssh_conn_string_array = []
		for r in reservations:
			for i in r.instances:
				if str(i.state) == 'running' and 'Name' in str(i.tags):
					if instance_name in str(i.tags['Name']):
						print str(i.tags['Name']), i.id, i.ip_address, i.private_ip_address, i.key_name , str(i.ip_address), str(i.instance_type),aws_region
						ssh_key_file = search_files(str(i.key_name+"*"),key_directory)
						if str(i.ip_address) == 'None' and len(ssh_key_file) > 0 :
							ssh_cmd = 'ssh -oStrictHostKeyChecking=no -oTCPKeepAlive=yes -oServerAliveInterval=50  -i {0} ubuntu@{1} '.format(ssh_key_file[0],i.private_ip_address)
							print ssh_cmd
							ssh_commands_list.append(ssh_cmd)
						elif (len(ssh_key_file) > 0):
							ssh_cmd = 'ssh -oStrictHostKeyChecking=no -oTCPKeepAlive=yes -o ServerAliveInterval=50  -i {0} ubuntu@{1} '.format(ssh_key_file[0],i.ip_address)
							print ssh_cmd
							ssh_commands_list.append(ssh_cmd)

						else:
							ssh_commands_list.append(ssh_cmd)
							print "Could n0t find SSH key pair \nssh -oStrictHostKeyChecking=no -i " + i.key_name + ' -l ubuntu ' + i.ip_address
							#exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--account', required=True, help='AWS ACCOUNT')
	parser.add_argument('-n', '--name', required=True, help='INSTANCE_NAME' )
	args = parser.parse_args()
	if args.account and args.name:
		search_instances(args.name, args.account)
		time.sleep(2)
		if (len(ssh_commands_list) >= 1):
			random.shuffle(ssh_commands_list)
			p = subprocess.call(ssh_commands_list[0], shell=True)
