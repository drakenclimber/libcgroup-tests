#
# Config class for the libcgroup functional tests
#
# Copyright (c) 2019 Oracle and/or its affiliates.  All rights reserved.
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

import consts
from container import Container
import os

class Config(object):
    def __init__(self, args, container=None):
        self.args = args

        if self.args.container:
            if container:
                self.container = container
            else:
                # Use the default container settings
                self.container = Container(name=consts.DEFAULT_CONTAINER_NAME,
                    stop_timeout=args.timeout, arch=None,
                    distro=args.distro, release=args.release)

        self.ftest_dir = os.path.dirname(os.path.abspath(__file__))
        self.libcg_dir = os.path.dirname(self.ftest_dir)

        self.test_suite = consts.TESTS_RUN_ALL_SUITES
        self.test_num = consts.TESTS_RUN_ALL
        self.verbose = False

    def __str__(self):
        out_str = "Configuration"
        if self.args.container:
            out_str += "\n\tcontainer = {}".format(self.container)

        return out_str


class ConfigError(Exception):
    def __init__(self, message):
        super(ConfigError, self).__init__(message)

    def __str__(self):
        out_str = "ConfigError:\n\tmessage = {}".format(self.message)
        return out_str
