#!/usr/bin/python
'''
High resolution timer for the gethostbyname() call to our dns servers.  
Does not fork a 'dig' subprocess

'''
import socket, time, sys, os
sys.path.append('/usr/local/tcollector/collectors/lib')
import utils
import signal

timer = time.time
debug = 1
requestList = []
requestList.append('www.ticketmaster.com')
requestList.append('probe.tm.tmcs')

COLLECTOR_INTERVAL = 15

'''
Would be great to put the timer functions in a tmlib.  Fucntions
are more general than the task requires
'''
def total(reps, func, *pargs, **kargs):
   '''
   Total time to run func() reps times.
   Returns (total time, last result)
   '''
   repslist = list(range(reps))
   start = timer()
   for i in repslist:
      ret = func(*pargs, **kargs)
   elapsed = timer() - start
   return (elapsed, ret)

def bestof(reps, func, *pargs, **kargs):
   '''
   Quickest func() among reps runs.
   Returns (best time, last result)
   '''
   best = 2 ** 32
   for i in range(reps):
      start = timer()
      ret = func(*pargs, **kargs)
      elapsed = timer() - start
      if elapsed < best: best = elapsed
      return (best, ret)

def bestoftotal(reps1, reps2, func, *pargs, **kargs):
   '''
   Best of totals:
   (bet of reps1 runs of (total of reps2 run of func))
   '''
   return bestof(reps1, total, reps2, func, *pargs, **kargs)

def trunc(f, n):
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

def signal_handler(signal, frame):
   sys.exit(0)

def main():
   utils.drop_privileges()
   while (True):
      signal.signal(signal.SIGINT, signal_handler)

      for name in requestList: 
         ts = int(time.time())
         '''
         Try to resolve the name.  if it succeeds, give the time it 
         took for the call to return.  if it fails don't put anything 
         in the metric, add a count of 1 to the failure count, which we 
         can graph seperately.  Since the failures aren't included in the 
         latency graph, whatever arbitrary value we choose won't skew TSD's
         averaging across groups up or down -- we just count the failures
         '''
         try:
            response = total(1, socket.gethostbyname, name)
            print 'dns.latencyms', ts, response[0] * 1000, 'target=' + name
            print 'dns.latencyms.failure', ts, '0', 'target=' + name
         except:
            response = '1'
            print 'dns.latencyms.failure', ts, response, 'target=' + name

      time.sleep(COLLECTOR_INTERVAL)


if __name__ == "__main__":
    main()
