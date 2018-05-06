# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:20:02 alex>
#

"""Init file of the Scaleway class definition"""

from sw_keys import AUTH_TOKEN, REGION

from .CScaleway import CScaleway
scaleway = CScaleway(AUTH_TOKEN, REGION)
