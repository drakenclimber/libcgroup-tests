#!/usr/bin/env python3
#
# Advanced cgset functionality test - set multiple values in multiple cgroups
#                                     via the '-r' flag
#
# Copyright (c) 2021 Oracle and/or its affiliates.
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
import sys

CONTROLLER = 'memory'
CGNAMES = ['026cgset1', '026cgset2']

SETTINGS = ['memory.limit_in_bytes',
            'memory.soft_limit_in_bytes',
            'memory.swappiness']
VALUES = ['2048000', '1024000', '89']

def prereqs(config):
    result = consts.TEST_PASSED
    cause = None

    if CgroupVersion.get_version('memory') != CgroupVersion.CGROUP_V1:
        result = consts.TEST_SKIPPED
        cause = "This test requires the cgroup v1 memory controller"
        return result, cause

    return result, cause

def setup(config):
    for cg in CGNAMES:
        Cgroup.create(config, CONTROLLER, cg)

def test(config):
    result = consts.TEST_PASSED
    cause = None

    Cgroup.set(config, cgname=CGNAMES, setting=SETTINGS, value=VALUES)

    for i, setting in enumerate(SETTINGS):
        for cg in CGNAMES:
            value = Cgroup.get(config, cgname=cg, setting=setting,
                               print_headers=False, values_only=True)

            if value != VALUES[i]:
                result = consts.TEST_FAILED
                cause = "Expected {} to be set to {} in {}, but received {}".format(
                    setting, VALUES[i], cg, value)
                return result, cause

    return result, cause

def teardown(config):
    for cg in CGNAMES:
        Cgroup.delete(config, CONTROLLER, cg)

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
