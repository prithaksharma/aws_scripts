#!/usr/local/bin/ipython
import os
from datetime import datetime, timedelta
import boto
import sys
access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
current_date = datetime.now()
try:
    c = boto.connect_iam(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    server_ssl_certs = c.list_server_certs()
    for cert_details in server_ssl_certs['list_server_certificates_response']['list_server_certificates_result']['server_certificate_metadata_list']:
        #print cert_details['arn'] ,  cert_details['expiration'], cert_details['server_certificate_id'] , cert_details['server_certificate_name']
        print  cert_details['expiration'], cert_details['server_certificate_name']
        ssl_cert_exipry_date = datetime.strptime(str(cert_details['expiration']), '%Y-%m-%dT%H:%M:%SZ')
        if ssl_cert_exipry_date <  current_date:
            print "{0}\t{1}\t{2}\t{3}".format(cert_details['arn'] ,  cert_details['expiration'], cert_details['server_certificate_id'] , cert_details['server_certificate_name'])
            print "Removing {}".format(cert_details['server_certificate_name'])
            #output = c.delete_server_cert(str(cert_details['server_certificate_name']))
            #print output
            #sys.exit(0)
except Exception, exc:
  print "An Error Occured\n {0}".format(exc)
  sys.exit(1)
