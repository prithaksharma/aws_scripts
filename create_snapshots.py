#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import boto.ec2
import sys
from datetime import datetime, timedelta
import smtplib

##keep snapshot worth of 2 days
no_of_days = 2
regions = ['eu-west-1']
crowd_filter = {'tag:Name': ['CROWD2_*', 'jira_installed_*']}
delete_time = datetime.utcnow() - timedelta(days=no_of_days)
FROM='EBS_SNAPSHOT_BACKUP_REPORT <backup_agent@example.com>'
TO=['sysadmins@example.com']
SUBJECT='EBS SNAPSHOT BACKUP REPORT'
msg=''

for reg in regions:
    conn = boto.ec2.connect_to_region(reg)
    volumes = conn.get_all_volumes(filters=crowd_filter) 
    for vols in volumes:
      print "id:{0} created_time:{1} status:{2} size:{3} type:{4} instance_id:{5}".format(vols.id,vols.create_time,vols.status,vols.size,vols.type,vols.attach_data.instance_id)
      if no_of_days > 0: 
         snap = conn.create_snapshot(vols.id,description='CREATEDBYBACKUPSCRIPT',dry_run=False)
	 print 'Creating snapshot\n Status: Pending'
	 while snap.status == 'pending':
	   #print snap.status
	   snap.update(2)
	   sleep(5)
	 #print snap.status
	 #print 'Snapshot created for Volume {0} with ID: {1}'.format(vols.id,snap.id)
	 msg = msg + 'Snapshot created for Volume {0} with ID: {1}\n'.format(vols.id,snap.id) 
	 snap.add_tags({'Type':'CREATED_BY_BACKUP_SCRIPT'})
    snapshots = conn.get_all_snapshots(filters= {'tag:Type':'CREATED_BY_BACKUP_SCRIPT'})
    for s in snapshots:
      start_time = datetime.strptime(s.start_time, '%Y-%m-%dT%H:%M:%S.000Z')
      if start_time <= delete_time:
        msg = msg + "Deleting SNAPSHOT - ID:{0} Description:{1} Region:{2} Start:{3} DelDate:{4}\n".format(s.id,s.description,s.region,s.start_time,str(delete_time))
        s.delete(dry_run=False)
MESSAGE = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, msg)
try:
  server = smtplib.SMTP("smtp.gmail.com", 587)
  #server.set_debuglevel(True)
  server.ehlo()
  server.starttls()
  server.login('backup_agent@example.com', 'xxxxxxxxxxxxx')
  server.sendmail(FROM, TO, MESSAGE)
  server.close()
  print 'Email Report Sent Successfully'
except:
  print 'Failed to send E-mail'
