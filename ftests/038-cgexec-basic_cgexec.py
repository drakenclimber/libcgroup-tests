#!/usr/bin/env python3
#
# Cgroup recursive cgdelete functionality test
#
# Copyright (c) 2020-2021 Oracle and/or its affiliates.
# Author: Tom Hromatka <tom.hromatka@oracle.com>
#

#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, see <http://www.gnu.org/licenses>.
#

from cgroup import Cgroup, CgroupVersion
import consts
import ftests
import os
from process import Process
import sys

import time

CONTROLLER = 'cpuset'
CGNAME = '038cgexec'

pid = None

def prereqs(config):
    # This test should run on both cgroup v1 and v2
    return consts.TEST_PASSED, None

def setup(config):
    Cgroup.create(config, CONTROLLER, CGNAME)

def test(config):
    global pid

    config.process.create_process_in_cgroup2(config, CONTROLLER, CGNAME)

    #proc_list = Cgroup.get(config, setting='cgroup.procs', cgname=CGNAME,
    #                       print_headers=False, values_only=True)
    pid = Cgroup.get_procs_in_cgroup(config, CGNAME, CONTROLLER)
    print("pid = {}".format(pid))

    if pid is None:
        result = consts.TEST_FAILED
        cause = "No processes were found in cgroup {}".format(CGNAME)
        return result, cause

    return consts.TEST_PASSED, None

def teardown(config):
    Cgroup.delete(config, CONTROLLER, CGNAME)

def main(config):
    [result, cause] = prereqs(config)
    if result != consts.TEST_PASSED:
        return [result, cause]

    setup(config)
    [result, cause] = test(config)
    teardown(config)

    return [result, cause]

if __name__ == '__main__':
    config = ftests.parse_args()
    # this test was invoked directly.  run only it
    config.args.num = int(os.path.basename(__file__).split('-')[0])
    sys.exit(ftests.main(config))
