"""Capture useful descriptive information about a fastq file.
"""
import hashlib
import os
import re
from collections import namedtuple, Counter

LaneID = namedtuple('LaneID', ['flowcell', 'lane', 'end', 'multiplex'])

class FastqSummary:
    def __init__(self, name=None):
        self.filename = name
        self.md5sum = None
        self.reads = None
        self.lengths = None

    def distance(self, b):
        return distance(self, b)

    def __repr__pretty__(self):
        rows = [self.md5sum + " " + str(self.filename)]
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

    def read_fastq(self, stream):
        """Parse a fastq stream
        """
        self.reads = Counter()
        self.length = Counter()
        md5 = hashlib.md5()
        delims = re.compile('[: ]')
        for count, line in enumerate(stream):
            md5.update(line)
            if 0 == count % 4:
                fields = delims.split(line)
                if len(fields) > 10:
                    fcid = fields[2]
                    lane = fields[3]
                    end = fields[7]
                    multiplex = fields[10].rstrip()
                    laneid = LaneID(fcid, lane, end, multiplex)
                    self.reads[laneid] += 1
                else:
                    self.reads[None] += 1
            elif 1 == count % 4:
                self.length[len(line.rstrip())] += 1

        self.md5sum = md5.hexdigest()

    def parse_pretty(self, record):
        self.reads = Counter()
        split_re = re.compile(':? ')
        header = record[0].rstrip()
        self.md5sum, self.filename = header.split(' ')

        for line in record[1:]:
            line = line[2:].rstrip()
            name, reads = line.split(': ')
            lane_id = parse_lane_id(name)
            self.reads[lane_id] = int(reads)

def format_lane_id(lane_id):
    if lane_id is None:
        return "None"
    else:
        return '_'.join(lane_id)


def parse_lane_id(token):
    if token == 'None':
        return None
    else:
        records = token.split('_')
        if len(records) != 4:
            raise RuntimeError(
                "lane ids are made of 4 components got: %d" % (len(records)))
        return LaneID(*records)

def distance(a, b):
    """Compute a distance between two fastq summaries

    Returns 0 if they are equal, 1 if they have nothing in common.
    """
    if a.md5sum == b.md5sum:
        return 0

    aset = set(a.reads.keys())
    bset = set(b.reads.keys())
    size = len(aset.union(bset))

    intersection = aset.intersection(bset)

    incommon = 0
    for k in intersection:
        counts = sorted([a.reads[k], b.reads[k]])
        error = (counts[1] - counts[0]) / float(counts[1])
        incommon += 1 - error

    return (size-incommon)/float(size)

def chunkify_pretty_stream(stream):
    record = [stream.readline()]
    for line in stream:
        if line.startswith('  '):
            record.append(line)
        else:
            yield record
            record = [line]
    yield record

def read_pretty(stream):
    """Read a pretty formatted report
    """
    for record in chunkify_pretty_stream(stream):
        f = FastqSummary()
        f.parse_pretty(record)
        yield f
