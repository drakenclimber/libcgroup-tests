#!/usr/bin/env python3
#
# Basic cgsnapshot functionality test
#
# Copyright (c) 2020 Oracle and/or its affiliates.
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

CONTROLLER='memory'
CGNAME="004cgsnapshot"
CGSNAPSHOT = """group 004cgsnapshot {
                    memory {
                            memory.use_hierarchy="1";
                            memory.soft_limit_in_bytes="9223372036854771712";
                            memory.force_empty="";
                            memory.move_charge_at_immigrate="0";
                            memory.kmem.tcp.max_usage_in_bytes="0";
                            memory.max_usage_in_bytes="0";
                            memory.oom_control="oom_kill_disable 0
                                under_oom 0
                                oom_kill 0"; 
                            memory.limit_in_bytes="9223372036854771712";
                            memory.swappiness="60";
                            memory.kmem.failcnt="0";
                            memory.kmem.max_usage_in_bytes="0";
                            memory.failcnt="0";
                            memory.kmem.tcp.failcnt="0";
                            memory.kmem.limit_in_bytes="9223372036854771712";
                            memory.use_hierarchy="1";
                            memory.kmem.tcp.limit_in_bytes="9223372036854771712";
                            memory.memsw.failcnt="0";
                            memory.memsw.limit_in_bytes="9223372036854771712";
                            memory.memsw.max_usage_in_bytes="0";
                    }
            }"""

def prereqs(config):
    result = consts.TEST_PASSED
    cause = None

    if CgroupVersion.get_version('memory') != CgroupVersion.CGROUP_V1:
        result = consts.TEST_SKIPPED
        cause = "This test requires the cgroup v1 memory controller"
        return result, cause

    if not config.args.container:
        result = consts.TEST_SKIPPED
        cause = "This test must be run within a container"
        return result, cause

    return result, cause

def setup(config):
    Cgroup.create(config, CONTROLLER, CGNAME)

def test(config):
    result = consts.TEST_PASSED
    cause = None

    expected = Cgroup.snapshot_to_dict(CGSNAPSHOT)
    actual = Cgroup.snapshot(config, controller=CONTROLLER)

    if expected[CGNAME] != actual[CGNAME]:
        result = consts.TEST_FAILED
        cause = "Expected cgsnapshot result did not equal actual cgsnapshot"

    return result, cause

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
