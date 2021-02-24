#!/usr/bin/env python3
#
# Basic cgxget functionality test
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
from run import RunError
import sys

CONTROLLER = 'cpu'
CGNAME = '017cgxget'

V1_SETTING = 'cpu.shares'
V1_VALUE = '512'

V2_SETTING = 'cpu.weight'
V2_VALUE = '50'

def prereqs(config):
    result = consts.TEST_PASSED
    cause = None

    if CgroupVersion.get_version('cpu') != CgroupVersion.CGROUP_V1:
        result = consts.TEST_SKIPPED
        cause = "This test requires the cgroup v1 cpu controller"

    # Github Actions has issues with cgxget and the code coverage profiler.
    # This causes issues with the error handling of this test
    if not config.args.container:
        result = consts.TEST_SKIPPED
        cause = "This test cannot be run outside of a container"
        return result, cause

    return result, cause

def setup(config):
    Cgroup.create(config, CONTROLLER, CGNAME)
    Cgroup.set(config, CGNAME, V1_SETTING, V1_VALUE)

def test(config):
    result = consts.TEST_PASSED
    cause = None

    # $ cgxget -r cpu.shares 017cgxget
    # 017cgxget:
    # cpu.shares: 512
    expected = "{}:\n{}: {}".format(CGNAME, V1_SETTING, V1_VALUE)
    out = Cgroup.xget(config, controller=None, cgname=CGNAME,
                      setting=V1_SETTING, print_headers=True,
                      values_only=False)
    if out != expected:
        result = consts.TEST_FAILED
        cause = "cgxget expected {} but received {}".format(expected, out)

    # $ cgxget -1 -n -r cpu.shares 017cgxget
    # cpu.shares: 512
    expected = "{}: {}".format(V1_SETTING, V1_VALUE)
    out = Cgroup.xget(config, controller=None, cgname=CGNAME,
                      setting=V1_SETTING, print_headers=False,
                      values_only=False, version=CgroupVersion.CGROUP_V1)
    if out != expected:
        result = consts.TEST_FAILED
        cause = "cgxget expected {} but received {}".format(expected, out)

    # $ cgxget -2 -n -r cpu.weight 017cgxget
    # cpu.weight: 50
    expected = "{}: {}".format(V2_SETTING, V2_VALUE)
    out = Cgroup.xget(config, controller=None, cgname=CGNAME,
                      setting=V2_SETTING, print_headers=False,
                      values_only=False, version=CgroupVersion.CGROUP_V2)
    if out != expected:
        result = consts.TEST_FAILED
        cause = "cgxget expected {} but received {}".format(expected, out)

    # Provide an invalid combination of a v1 setting and a v2 flag
    # $ cgxget -2 -n -r cpu.shares 017cgxget
    try:
        out = Cgroup.xget(config, controller=None, cgname=CGNAME,
                          setting=V1_SETTING, print_headers=False,
                          values_only=False, version=CgroupVersion.CGROUP_V2)
    except RunError as re:
        if re.ret != 93:
            result = consts.TEST_FAILED
            cause = "Expected return code of 93 but received {}".format(
                    re.ret)
            return result, causea
    else:
        result = consts.TEST_FAILED
        cause = "cgxget -2 -n -r cpu.shares 017cgxget erroneously passed"
        return result, cause

    # Provide an invalid combination of a v2 setting and a v1 flag
    # $ cgxget -1 -n -r cpu.weight 017cgxget
    try:
        out = Cgroup.xget(config, controller=None, cgname=CGNAME,
                          setting=V2_SETTING, print_headers=False,
                          values_only=False, version=CgroupVersion.CGROUP_V1)
    except RunError as re:
        if not "variable file read failed No such file or directory" in re.stderr:
            result = consts.TEST_FAILED
            cause = "Expected 'No such file...' to be in stderr"
            return result, causea

        if re.ret != 96:
            result = consts.TEST_FAILED
            cause = "Expected return code of 93 but received {}".format(
                    re.ret)
            return result, causea
    else:
        result = consts.TEST_FAILED
        cause = "cgxget -2 -n -r cpu.shares 017cgxget erroneously passed"
        return result, cause
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
