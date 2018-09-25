#!/usr/bin/env python
# title           : main.py
# description     : Count 1GCC, 2GCC, 3GCC, 4GCC from multiple GC log files
# author          : Fadhil I. Kurnia
# date            : September 25, 2018
# version         : 0.1
# usage           : see readme
# notes           :
# python_version  : 2.7.15+
#==============================================================================

import sys
import glob
import bisect


#===================== Begin of Class and Global Variable =====================

IS_DEBUG = False

INPUT_PATH = "input/*.dat"
GC_IDX_START_TIME = 6
GC_IDX_END_TIME = 7
TIME_UNIT = "ns"

class GCTime:
    start = 0
    end = 0

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start

class Statistics:
    num_disk = 0
    num_gc = 0
    min_time = 0
    max_time = 0
    gcc_time = 0
    gcc_data = []

    def display(self):
        print "\nAnalytics results: "
        print "==================================================="
        print " Number of disk : ", self.num_disk
        print " Number of individual GC process : ", self.num_gc
        print " Minimum time : ", self.min_time
        print " Maximum time : ", self.max_time
        print " Duration of GCC :"
        for i, ngcc in enumerate(self.gcc_data):
            percentage = float(ngcc) / float(self.max_time) * float(100) 
            print "   GCC %d : %ld \t(%.5f %%)" % (i, ngcc, percentage)
        print "===================================================\n"

#====================== End of Class and Global Variable ======================


def accumulateGCC(stat, start, end, ngc):
    stat.gcc_data[ngc-1] += (end-start)
    if IS_DEBUG :
        print start, end, ngc
    return

def processLogFiles():
    gc_logfilenames = sorted(glob.glob(INPUT_PATH))
    num_files = len(gc_logfilenames)
    gcs = []

    # read all the gc in logfiles and put it on gcs[]
    for logfilename in gc_logfilenames:
        logfile = open(logfilename)
        logfilelines = logfile.readlines()

        for line in logfilelines:
            gc_raw = str(line)
            gc_token = gc_raw.split()

            start_time = gc_token[GC_IDX_START_TIME]
            end_time = gc_token[GC_IDX_END_TIME]

            bisect.insort(gcs, GCTime(long(start_time), long(end_time)))
    
    return [num_files, gcs]

def countGCC(ndisk, gc_data):
    stat = Statistics()

    stat.num_disk = ndisk
    stat.gcc_data = [0] * ndisk
    stat.min_time = gc_data[0].start
    stat.max_time = gc_data[0].end
    stat.num_gc = len(gc_data)
    
    crt_time = stat.min_time
    crt_depth = 1
    pqueue = []

    # counting one gc at a time
    for i in range(stat.num_gc):
        
        # handle first data
        if i == 0:
            pqueue.append(gc_data[i].start)
        
        # handle data in the middle
        if gc_data[i].start < pqueue[0]:
            if crt_time != gc_data[i].start:
                accumulateGCC(stat, crt_time, gc_data[i].start, crt_depth)
            crt_time = gc_data[i].start
            bisect.insort(pqueue, gc_data[i].end)
            crt_depth += 1
        elif gc_data[i].start == pqueue[0]:
            if crt_time != gc_data[i].start:
                accumulateGCC(stat, crt_time, gc_data[i].start, crt_depth)
            crt_time = gc_data[i].start
            bisect.insort(pqueue, gc_data[i].end)
            pqueue.pop(0)
        else:
            while len(pqueue) > 0 and pqueue[0] < gc_data[i].start:
                accumulateGCC(stat, crt_time, pqueue[0], crt_depth)
                crt_time = pqueue.pop(0)
                crt_depth -= 1
            accumulateGCC(stat, crt_time, gc_data[i].start, crt_depth)
            stat.gcc_data[crt_depth-1] += 1
            crt_time = gc_data[i].start
            bisect.insort(pqueue, gc_data[i].end)
            crt_depth += 1

        # handle last data
        if i == stat.num_gc-1 :
            while len(pqueue) > 0 :
                if crt_time != pqueue[0]:
                    accumulateGCC(stat, crt_time, pqueue[0], crt_depth)
                crt_time = pqueue.pop(0)
                crt_depth -= 1
            stat.max_time = crt_time

    return stat


if __name__ == "__main__":

    print("reading gc log data ...")
    log_data = processLogFiles()
    print("counting gcc...")
    statistic = countGCC(log_data[0], log_data[1])

    statistic.display()
