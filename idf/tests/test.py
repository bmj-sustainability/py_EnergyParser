#===============================================================================
# Set up
#===============================================================================
# Standard:

from config import *

import logging.config
import unittest

from os import sys, path


# Add parent to path
if __name__ == '__main__' and __package__ is None:
    this_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))



from utility_inspect import get_self
from utilities_xml import get_table_all_names, print_table
from idf_parser import IDF
#import idf_parser as idf_parser
import utilities_xml as util_xml
import os.path as path

#===============================================================================
# Logging
#===============================================================================
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

import idf_parser as idf

#===============================================================================
# Directories and files
#===============================================================================
curr_dir = path.dirname(path.abspath(__file__))
DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)



#===============================================================================
# Unit testing
#===============================================================================
print("Test")
class BasicTest(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(get_self())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        
        #self.PATH_DESIGN_BUILDER = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\Design Builder model\export1.idf")
        #self.PATH_DESIGN_TRNSYS = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\TRNSYS model\simple r00.idf")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
        #print(self.PATH_DESIGN_BUILDER)
        #design_builder_idf = IDF.from_IDF_file(self.PATH_DESIGN_BUILDER)
        #trnsys_idf = IDF.from_IDF_file(self.PATH_DESIGN_TRNSYS)
        test_file_path = path.join(DIR_SAMPLE_IDF,"5ZoneElectricBaseboard.idf")
        logging.info("Test file:{}".format(test_file_path))
        test_idf = IDF.from_IDF_file(test_file_path)
        
        print("All objects:")
        table_names = util_xml.get_table_all_names(test_idf)
        #print(table_names)
        util_xml.print_table(table_names)
        print("Number of objects:")
        table_counts = util_xml.get_table_object_count(test_idf)
        util_xml.print_table(table_counts)
        print(test_idf.num_objects)

        print("*** Loaded ***\n",test_idf)
        print("*** ****** ***\n")


