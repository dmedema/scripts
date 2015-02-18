#!/usr/bin/python

"""A way to gather heartbeats for TSDB, eg. to view uptime reports"""

import sys
import time

from collectors.lib import utils

COLLECTION_INTERVAL = 60  # seconds

def main():
	"""Uptime main loop."""
	utils.drop_privileges()

	counter = 0

	while True:
		ts = int(time.time())
		print ("%s %d %s" % ("proc.uptime.heartbeat",ts,counter))
		counter += 1
		sys.stdout.flush()
		time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
	main()
