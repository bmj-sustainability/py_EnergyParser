#===============================================================================
# Set up
#===============================================================================
# Standard:



from config.config_template import *

import logging.config
import unittest

from ExergyUtilities.utility_inspect import get_self
from idf.utilities_xml import get_table_all_names, print_table
from idf.idf_parser import IDF
import os.path as path

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class BasicTest(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(get_self())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        self.PATH_DESIGN_BUILDER = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\Design Builder model\export1.idf")
        self.PATH_DESIGN_TRNSYS = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\TRNSYS model\simple r00.idf")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
        print(self.PATH_DESIGN_BUILDER)
        design_builder_idf = IDF.from_IDF_file(self.PATH_DESIGN_BUILDER)
        trnsys_idf = IDF.from_IDF_file(self.PATH_DESIGN_TRNSYS)
        
        this_table = get_table_all_names(design_builder_idf)
        print_table(this_table)
        #print(design_builder_idf)
        #print(IDF())
        

