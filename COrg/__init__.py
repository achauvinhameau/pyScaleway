# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:13:46 alex>
#

"""Init file of the CImages class definition"""

# from main import __version__
from CScaleway import scaleway
from .COrg import COrg

organization = COrg(scaleway)
