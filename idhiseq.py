#!/usr/bin/python
"""Attempt to describe a fastq file generated on a highseq
"""
from __future__ import print_function
from argparse import ArgumentParser
from collections import namedtuple, Counter
from htsworkflow.util.opener import autoopen
import hashlib
import os
from pprint import pprint
import re
import sys


LaneID = namedtuple('LaneID', 'flowcell lane end multiplex')

def main(cmdline=None):
    parser = make_parser()
    args = parser.parse_args(cmdline)
    for filename in args.filenames:
        with autoopen(filename, 'r') as instream:
            fastq_info = parse_fastq(instream)
            fastq_info.filename= os.path.abspath(filename)
            if args.csv:
                print(fastq_info.__repr__csv__())
            else:
                print(fastq_info.__repr__pretty__())

def parse_fastq(stream):
    reads = Counter()
    length = Counter()
    md5 = hashlib.md5()
    delims = re.compile('[: ]')
    for count, line in enumerate(stream):
        md5.update(line)
        if 0 == count % 4:
            fields = delims.split(line)
            fcid = fields[2]
            lane = fields[3]
            end = fields[7]
            multiplex = fields[10].rstrip()
            laneid = LaneID(fcid, lane, end, multiplex)
            reads[laneid] += 1
        elif 1 == count % 4:
            length[len(line.rstrip())] += 1

    fastq = FastqDescription()
    fastq.md5sum = md5.hexdigest()
    fastq.reads = reads
    fastq.lengths = length
    return fastq

def format_lane_id(lane_id):
    return '_'.join(lane_id)

class FastqDescription:
    def __init__(self):
        self.filename = None
        self.md5sum = None
        self.reads = None
        self.lengths = None

    def __repr__pretty__(self):
        rows = [self.md5sum + " " + self.filename]
        for name in sorted(self.reads):
            rows.append('  {}: {}'.format(format_lane_id(name),
                                         self.reads[name]))
        return os.linesep.join(rows)
        
    def __repr__csv__(self):
        rows = []
        for name in sorted(self.reads):
            row = [self.filename, self.md5sum, 
                   format_lane_id(name), 
                   str(self.reads[name])]
            rows.append(','.join(row))
        return os.linesep.join(rows)
        
def make_parser():
    parser = ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--turtle', default=False, action='store_true',
                        help='output description as turtle')
    parser.add_argument('--csv', default=False, action='store_true',
                        help='output description as csv')
    return parser
    
if __name__ == "__main__":
    main(sys.argv[1:])
