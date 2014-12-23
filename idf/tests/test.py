#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

#from utility_inspect import whoami,  listObject

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class DesignSpaceBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

