#!/usr/bin/python
import subprocess
import sys
import os


### add more DATABASES here
### EXAMPLE MYSQL DB
users = {
 'db_host' : 'db_host1.us-west-1.rds.amazonaws.com',
 'db_name' : 'users',
 'db_password' : 'db_password',
 'db_user':'db_user',
 'db_type' : 'mysql'
}


### Example PGSql RDS instance
catalog = {
 'db_host' : 'db-host2.us-west-1.rds.amazonaws.com',
 'db_name' : 'catalog',
 'db_password' : 'db_password',
 'db_user' : 'db_user',
 'db_type' : 'pgsql'

 }

#### add more database here
list_of_dbs = [ users, catalog ]
list_of_files = []
def backup_dbs():
    for dbs in list_of_dbs:
        print 'Backing UP : {0}'.format(dbs['db_name'])
        if dbs['db_type'] == 'mysql':
            command = 'mysqldump --single-transaction -u {0} -h {1} -p{2}  {3} > {4}.sql'.format(dbs['db_user'],dbs['db_host'],dbs['db_password'],dbs['db_name'],dbs['db_name'])
            p = subprocess.Popen([command],stdout=subprocess.PIPE, shell=True)
            stdout = p.communicate()
            file_name = dbs['db_name'] + '.sql'
            list_of_files.append(file_name)
        elif dbs['db_type'] == 'pgsql':
            command = 'PGPASSWORD={0} pg_dump --no-owner --no-privileges --create --clean  -h {1} -U {2} {3}  > {4}.sql'.format(dbs['db_password'],dbs['db_host'],dbs['db_user'],dbs['db_name'],dbs['db_name'])
            print command
            p = subprocess.Popen([command],stdout=subprocess.PIPE, shell=True)
            stdout = p.communicate()
            file_name = dbs['db_name'] + '.sql'
            list_of_files.append(file_name)

def upload_to_s3():
    ## use IAM roles, if not then enable the following but its a bad practice
    #os.environ["AWS_ACCESS_KEY_ID"] = 'AWS_ACCESS_KEY'
    #os.environ["AWS_SECRET_ACCESS_KEY"] = 'AWS_SECRET_KEY'
    #os.environ["AWS_DEFAULT_REGION"] = 'us-west-1'
    for file_name in list_of_files:
        command = '/usr/bin/aws s3 cp {0}  s3://stagingdbs/daily_database_dump/{1}'.format(file_name,file_name)
        print command
        p = subprocess.Popen([command],stdout=subprocess.PIPE, shell=True)
        stdout = p.communicate()
        for i in stdout:
            print i

if __name__ == "__main__":
    backup_dbs()
    upload_to_s3()
