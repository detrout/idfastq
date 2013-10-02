# Author: Diane Trout
# Date: 2013 Sept 27
#
# This file contains the initialization information from the autoopen package.
#
# Copyright (c) 2013 by California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the California Institute of Technology nor
# the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior
# written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CALTECH
# OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
#

from __future__ import print_function

try:
    from setuptools import setup
except ImportError:
    print('falling back on distutils')
    from distutils.core import setup

setup(name='idfastq',
      version='0.1',
      description='Help identify the contents of an illumina hiseq fastq file',
      long_description="""This was my effort to try and understand multiple 
slighly varying fastq files. By finding counting common read identifiers
from the each file.

I took a shortcut by assuming that all the fastq files were illumina 
formatted. The read ID that was then grouped on flowcell / lane / end /
multiplex id. 
      """,
      author='Diane Trout',
      author_email='diane@caltech.edu',
      install_requires=['autoopen >=0.1'],
      packages=['idfastq'],
      scripts=['identify-fastqs'],
      test_suite='idfastq.test.test_fastq_summary',
      )
