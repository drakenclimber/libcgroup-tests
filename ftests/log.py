#
# Log class for the libcgroup functional tests
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
import datetime
import log

log_level = consts.DEFAULT_LOG_LEVEL
log_file = consts.DEFAULT_LOG_FILE
log_fd = None


class Log(object):

    @staticmethod
    def log(msg, msg_level=consts.DEFAULT_LOG_LEVEL):
        if log_level >= msg_level:
            if log.log_fd is None:
                Log.open_logfd(log.log_file)

            timestamp = datetime.datetime.now().strftime('%b %d %H:%M:%S')
            log_fd.write("{}: {}\n".format(timestamp, msg))

    @staticmethod
    def open_logfd(log_file):
        log.log_fd = open(log_file, "a")

    @staticmethod
    def log_critical(msg):
        Log.log("CRITICAL: {}".format(msg), consts.LOG_CRITICAL)

    @staticmethod
    def log_warning(msg):
        Log.log("WARNING: {}".format(msg), consts.LOG_WARNING)

    @staticmethod
    def log_debug(msg):
        Log.log("DEBUG: {}".format(msg), consts.LOG_DEBUG)
