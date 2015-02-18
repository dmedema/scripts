#!/usr/bin/env python
###########################################################
# 
# This python script is used for mysql database backup
# using mysqldump utility.
# 
# Written by : Denise Lopez
# Create date: Sep 11 2014
# Last modified: Sep 11 2014
# Tested with : Python 2.7.6
# Script Revision: 1.1
#
###########################################################

# Import requiredy python libraries
import ConfigParser
import os
import time
import sys
import shutil

# On Debian, /etc/mysql/debian.cnf contains 'root' a like login and password.
config = ConfigParser.ConfigParser()
config.read("/etc/mysql/debian.cnf")
username = config.get('client', 'user')
password = config.get('client', 'password')
hostname = config.get('client', 'host')
nfs_path = '/var/lib/glance/images'
backup_path = '/var/lib/glance/images/mysql_backup/'
error_log = open('/var/log/mysql/backup_error.log',"w")
sys.stdout = error_log

filestamp = time.strftime('%Y-%m-%d')

# Separate directories for the backups YYYYMMDD
today_backup_path = backup_path + filestamp

# Check if the NFS mount exists, if not try to create it 
print "Checking if the NFS mount point exists"
if not os.path.exists(nfs_path):
  print "NFS mount doesn't exist, exiting with 1"
  sys.exit(1)

# Checking if backup folder exists. If not create it.
print "Creating backup folder" + today_backup_path
if not os.path.exists(today_backup_path):
    os.makedirs(today_backup_path)

# Get a list of databases with :
database_list_command="mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (username, password, hostname)
for database in os.popen(database_list_command).readlines():
    database = database.strip()
    if database == 'information_schema':
        continue
    if database == 'performance_schema':
        continue
    filename = today_backup_path + "/%s-%s.sql" % (database, filestamp)
    print "Backing up " + database
    if database == 'keystone':
        os.popen("mysqldump -u %s -p%s -h %s --ignore-table=keystone.token -e --opt -c %s | gzip -c > %s.gz" % (username, password, hostname, database, filename))
    else:
        os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz" % (username, password, hostname, database, filename))

# Clean up the backup directory and only save 7 days of backups
now = time.time()

for file_object in os.listdir(backup_path):
    file_object_path = os.path.join(backup_path, file_object)
    if os.stat(file_object_path).st_mtime < now - 7 * 86400:
        if os.path.isfile(file_object_path):
            print "Deleting " + os.path.join(backup_path, file_object)
            os.remove(os.path.join(backup_path, file_object))
        elif os.path.isdir(os.path.join(backup_path, file_object)):
            print "Deleting " + os.path.join(backup_path, file_object)
            shutil.rmtree(os.path.join(backup_path, file_object))

print "Backup complete " + filestamp

