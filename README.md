# aws_scripts

# Useful Python Scrips for AWS Sysadmins 
~~~
list_iam_certs_about_to_expire.py  -> Lists SSL Certs in IAM that are about to expire
create_snapshots.py  -> Creates EBS snapshots of running Instances based on the Instance TAG ; rotates the SNAPSHOTS as well
exectue_commands.py -> Executes arbitrary SSH commands on an instance based on Instance Name
ssh_aws.py -> Searches AWS instances based on Name tag, finds the SSH keys and automatically SSH into one of them
dump_rds_and_copy_to_s3.py -> Ugly Shell wrapper, backs up Postgres and MySQL RDS instances using mysqldump and pgsql utility and uploads to S3
~~~
error
