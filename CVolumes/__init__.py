# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:14:58 alex>
#

"""Init file of the CVolumes class definition"""

from CScaleway import scaleway
from .CVolumes import CVolumes

volumes = CVolumes(scaleway)
