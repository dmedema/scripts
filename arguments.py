#!/usr/bin/python
__author__ = 'DLo'
import sys
 
total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
# Pharsing args one by one 
print ("Script name: %s" % str(sys.argv[0]))

for i in xrange(total):
    print ("Argument # %d : %s" % (i, str(sys.argv[i]))) 
