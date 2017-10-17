# -*- coding:utf-8 -*-

from __future__ import print_function, absolute_import

import itertools


_cnt = itertools.count()
TYPE_REMOTE_SSH = next(_cnt)
TYPE_LOCAL = next(_cnt)

TYPE_RESOURCE_PROCESS = next(_cnt)
TYPE_RESOURCE_FILE = next(_cnt)
TYPE_RESOURCE_CONFIG = next(_cnt)

del _cnt
