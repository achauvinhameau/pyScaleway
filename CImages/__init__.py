# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:16:04 alex>
#

"""Init file of the CImages class definition"""

# from main import __version__
from CScaleway import scaleway
from .CImages import CImages

images = CImages(scaleway)
