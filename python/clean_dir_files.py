#!/usr/bin/python

import os, time, sys

backup_path = '/var/lib/glance/images/mysql_backup'

# Clean up the backup directory and only save 7 days of backups
now = time.time()

for file_object in os.listdir(backup_path):
    file_object_path = os.path.join(backup_path, file_object)
    if os.stat(file_object_path).st_mtime < now - 7 * 86400:
        if os.path.isfile(file_object_path):
            print os.path.join(backup_path, file_object)
            os.remove(os.path.join(backup_path, file_object))
        elif os.path.isdir(os.path.join(backup_path, file_object)):
            print os.path.join(backup_path, file_object)
            shutil.rmtree(os.path.join(backup_path, file_object))

