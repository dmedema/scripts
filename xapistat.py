#!/usr/bin/env python
""" A simple tcollector for Xen Hosts. This uses the rrd interface. 
    Reports memory, cpu, vm count, and network bandwidth.
    Here is a good reference on the Xen RRD: 
    http://community.citrix.com/display/xs/Using+XenServer+RRDs
"""
import sys
sys.path.append('/usr/local/tcollector/collectors/lib')

import time
import XenAPI
import parse_rrd
import socket
import re
import os
import logging

# globals
global_params = {
    'collection_interval' : 15,
    'verbose' : 0,
}

class metricsXAPI:
    def __init__(self, logger):
        self.logger = logger
        self.verbose = 0
        self.params = {}
        self.url = "http://localhost"
        self.x = XenAPI.xapi_local()
        try:
            self.x.login_with_password("root","")
            self.xapi = self.x.xenapi
            self.rrd_updates = parse_rrd.RRDUpdates()
            # hack - begin - rrd_updates has a bug where it overrides
            # the params passed in so here we set what we want 
            # kind of a monkey patch
            self.rrd_updates.params['interval'] = 5
            self.rrd_updates.params['start'] = int(time.time()) - 10 
            # hack - end 
            # this is if we ever upgrade to parse_rrd that does the right thing
            # the below are suppose to overload the defaults, they dont
            self.params['cf'] = "AVERAGE"
            self.params['start'] = int(time.time()) - 10
            self.params['interval'] = 5 # the interval at which the data is returned
            self.params['host'] = "true"
            self.rrd_updates.refresh(self.x.handle, self.params, self.url)

            ## get host uuid and ref
            self.host_uuid = self.rrd_updates.get_host_uuid()
            self.host_oRef = self.x.xenapi.host.get_by_uuid(self.host_uuid) 
        finally:
            self.x.logout()

    def logout(self):
            self.x.logout()
            self = None

    def get_resident_vm_count(self):
        self.logger.debug("HOST UUID: %s" % self.host_uuid) 
        resident_vm_cnt = len(self.x.xenapi.host.get_resident_VMs(self.host_oRef))
        self.output_data(self.mname_map('resident_vm_cnt'), self.epoch, resident_vm_cnt, {})

    def mname_map(self, metric):
        metric_names = { 
            "resident_vm_cnt"       : "xen.num_resident_vms",
            "loadavg"               : "xen.proc.stats.cpu.load",    # type=avg
            "cpu_avg"               : "xen.proc.stats.cpu",         # type=avg
            "per_cpu_stat"          : "xen.proc.stats.cpu.percpu",  # cpu=ID type=??
            "net_bytes_stat"        : "xen.proc.net.bytes",         # iface= direction=in|out
            "memory_free_kib"       : "xen.proc.meminfo.memfree",
            "memory_total_kib"      : "xen.proc.meminfo.memtotal" ,
            "memory_used_pct"       : "xen.proc.meminfo.memusedpct", 
            "xapi_free_memory_kib"  : "xen.xapi.meminfo.memfree", 
            "xapi_memory_usage_kib" : "xen.xapi.meminfo.memused", 
            "xapi_live_memory_kib"  : "xen.xapi.meminfo.memlive", 
            "xapi_allocation_kib"   : "xen.xapi.meminfo.memtotal", 
        }
        if metric in metric_names:
            return metric_names[metric]
        return False

    def get_latest_host_data(self, **key):
        cpure = re.compile(r"cpu\d+.*", re.I)
        memre = re.compile(r"pif.+", re.I)

        for param in self.rrd_updates.get_host_param_list():
            ## empty param
            if param == "":
                continue
            max_time = 0
            maxIndex = self.rrd_updates.get_nrows() - 1;
            self.logger.debug("Param: %s" % param)
            self.logger.debug("Range: %s" % self.rrd_updates.get_nrows())
            self.logger.debug("MaxIndex: %s" % maxIndex)

            epoch = self.rrd_updates.get_row_time(maxIndex)
            self.epoch = epoch

            data = float(self.rrd_updates.get_host_data(param,maxIndex))
            self.logger.debug("Row Data: %s Time Stamp: %s : %s" % 
                (self.mname_map(param), epoch, data))

            if param.startswith('pif'):
                match = re.search(r'(pif_[^_]+)_(rx|tx)', param)
                direction = 'unknown'
                if match.group(2) == 'rx':
                    direction = 'in'
                elif match.group(2) == 'tx':
                    direction = 'out'
                self.output_data(self.mname_map('net_bytes_stat'), epoch, data,
                    {'iface' : match.group(1), 'direction' : direction })

            elif cpure.match(param):
                cpu_num = re.match("cpu(\d+)", param)
                self.logger.debug("CPU: %s : %s" % (cpu_num, data))
                data *= 100
                self.output_data(self.mname_map('per_cpu_stat'), epoch, data,
                    {'cpu' : cpu_num.group(1)})

            elif param.startswith('xapi'):
                self.output_data(self.mname_map(param), epoch, int(data), 
                    {'type' : 'KB'})

            elif param == 'memory_total_kib':
                self.memory_total = int(data)
                self.output_data(self.mname_map(param), epoch, self.memory_total, 
                    {'type' : 'KB'})
                   
            elif param == 'memory_free_kib':
                self.memory_free = int(data)
                self.output_data(self.mname_map(param), epoch, self.memory_free,
                    {'type' : 'KB'})
            else:
                self.logger.debug("Not handled metric: %s" % param)
                if (self.mname_map(param)):
                    self.output_data(self.mname_map(param), epoch, data,{})
                
        #Lets make a human readable memory % for quick ref
        memory_used_pct = int(float((self.memory_total - self.memory_free)) 
            / self.memory_total * 100)
        self.output_data(self.mname_map('memory_used_pct'), self.epoch,
             memory_used_pct, {})

    def output_data(self, name, ts, val, tags):
        tag_str = ""
        for tagk in tags:
            tag_str += tagk + "=" + tags[tagk] + " "
        print("%s %d %s %s" % (name, ts, val, tag_str))

def verbose(logger):
    if global_params['verbose'] == 1:
       logger.setLevel(logging.DEBUG) 
       # CRITICAL, ERROR, WARNING, INFO, DEBUG

def logger_init():
    logger = logging.getLogger()
    verbose(logger)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def main():
    logger = logger_init()

    logger.debug("Starting Loop")
    while True:
       logger.debug("Loop Iteration")
       metrics = metricsXAPI(logger)
       metrics.get_latest_host_data()
       metrics.get_resident_vm_count()
       metrics.logout()
       metrics = None 
       logger.debug("EPOCH Time: %s" % time.time())
       sys.stdout.flush()
       time.sleep(global_params['collection_interval'])
    sys.exit()

if __name__ == "__main__":
    main()
    sys.exit()
