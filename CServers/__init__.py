# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:16:37 alex>
#

"""Init file of the CServers class definition"""

from CScaleway import scaleway
from .CServers import CServers

servers = CServers(scaleway)
