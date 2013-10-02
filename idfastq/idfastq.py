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

from .fastq_summary import FastqSummary

def main(cmdline=None):
    parser = make_parser()
    args = parser.parse_args(cmdline)
    for filename in args.filenames:
        with autoopen(filename, 'r') as instream:
            fastq_info = FastqSummary(os.path.abspath(filename))
            fastq_info.parse_fastq(instream)
            if args.csv:
                print(fastq_info.__repr__csv__())
            else:
                print(fastq_info.__repr__pretty__())


def make_parser():
    parser = ArgumentParser(
        '%prog: fastq_file...\n',
        'Generate a report of what HiSeq projects are in a fastq file',
    )
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('--turtle', default=False, action='store_true',
                        help='output description as turtle')
    parser.add_argument('--csv', default=False, action='store_true',
                        help='output description as csv')
    return parser
    
if __name__ == "__main__":
    main(sys.argv[1:])
