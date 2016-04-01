#!/usr/bin/env python
#coding: utf-8
import boto.ec2
import sys
import paramiko
import argparse


def find_instances(instance_name):
  list_of_instances = {} 
  if not instance_name:
    print "No Instances found"
    sys.exit(1) 
  try:
    conn = boto.ec2.connect_to_region('eu-west-1',aws_access_key_id='XXXXXX', aws_secret_access_key='XXXXX')
    reservations = conn.get_all_instances()
  except Exception, exc:
    print "An Error Occured\n {0}".format(exc)
    sys.exit(1)
  for res in reservations:
    for inst in res.instances:
      if str(inst.state).lower() == 'running' and 'Name' in str(inst.tags):
        if str(inst.tags['Name']) == instance_name:
          list_of_instances[inst.id] = { 'NAME' : instance_name ,'IPV4' : inst.private_ip_address  }
  return list_of_instances 

def execute_commands_over_ssh ( instance_ip, command='/sbin/ifconfig'):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    ssh.connect(instance_ip, port=22, username = 'ubuntu', key_filename = './YOUR_SSH_KEY_LOCATION.pem')
    print 'Executing command: {0}'.format(command)
    cmd = 'sudo ' + command
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print stdout.readlines()
    ssh.close()
    return stdin, stdout, stderr
  except Exception, excp:
    print "An Error Occured\n {0}".format(excp)
    sys.exit(1)
  
 
### starts from here
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--name', required=True)
  parser.add_argument('-c', '--command', required=True )
  args = parser.parse_args()
  inst_list = find_instances(args.name)
  if not inst_list:
    print 'Instance {0} not found'.format(args.name)
    sys.exit(1)
  else:
    print inst_list
    for key in inst_list:
      #print 'IP:{0}   ID:{1}\n'.format(inst_list[key]['IPV4'], key)
      #execute_commands_over_ssh(inst_list[key]['IPV4'], 'sudo /sbin/ifconfig')
      execute_commands_over_ssh(inst_list[key]['IPV4'], args.command)
      #print stdin.readlines(), stdout.readlines(), stderr.readlines()
