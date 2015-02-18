#!/usr/bin/python

import sys
import os 

error_log = open('test_error.log',"w")

sys.stdout = error_log 

print "testing writing to file"

backup_dir = '/home/ubuntu/testing'

if not os.path.exists(backup_dir):
  print "Backup directory doesn't exist"
  sys.exit(1)


