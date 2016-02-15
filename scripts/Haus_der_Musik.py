#===============================================================================
# Set up 
#===============================================================================

# Standard ----------------------------------------------------------------------
import os.path as path
from shutil import copyfile
import logging.config
import unittest
import sys

# Get self path
script_path = path.split(path.realpath(__file__))[0]
# Adjust to add the module path
module_path = path.normpath( script_path + "/.."  + "/idf")
# Add it 
sys.path.append(module_path)

#------------------------------------------------------------------------------ 
# Config
from config.config import *

# Modules
from ExergyUtilities.utility_inspect import get_self
import utilities_xml as utilXML 
from idf_parser import IDF
from kept_classes import keptClassesDict

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")


def main():
    PATH_DESIGN_BUILDER = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\Design Builder model\export1.idf")
    PATH_DESIGN_TRNSYS = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\TRNSYS model\simple r00.idf")
    PATH_TRNSYS_TEMPLATE = path.join(PATH_ENERGY_DB, r"IDF TRNSYS Conversion\TRNSYS_template.txt")
    idf_design_builder = IDF.from_IDF_file(PATH_DESIGN_BUILDER)
    idf_trnsys = IDF.from_IDF_file(PATH_DESIGN_TRNSYS)
    
    print("TRNSYS")
    this_table = utilXML.get_table_all_names(idf_trnsys)
    utilXML.print_table(this_table)

    print("DESIGN BUILDER")
    this_table = utilXML.get_table_all_names(idf_design_builder)
    utilXML.print_table(this_table)
    
    utilXML.clean_out_object(idf_design_builder,keptClassesDict["TRNSYS"])
    utilXML.clean_out_object(idf_trnsys,keptClassesDict["TRNSYS"])

    print("TRNSYS")
    this_table = utilXML.get_table_all_names(idf_design_builder)
    utilXML.print_table(this_table)

    print("DESIGN BUILDER")
    this_table = utilXML.get_table_all_names(idf_trnsys)
    utilXML.print_table(this_table)
    
    
    #with open(PATH_TRNSYS_TEMPLATE) as f:
    #    TEMPLATE = f.readlines()
    
    #print(path.split(PATH_TRNSYS_TEMPLATE))
    target_dir = path.split(PATH_TRNSYS_TEMPLATE)[0]
    target_file_name = "TRNSYS_idf_out.idf"
    target_path = path.join(target_dir, target_file_name)
    #print(target_path)
    
    copyfile(PATH_TRNSYS_TEMPLATE, target_path)
    logging.debug("Copied \n\t\t{} \n\t\t{}".format(PATH_TRNSYS_TEMPLATE,target_path))

    idf_design_builder.convert_XML_to_IDF()
    #print(idf_design_builder.IDF_string)

    with open(target_path, "a") as myfile:
        myfile.write(idf_design_builder.IDF_string)

    logging.debug("Wrote {}".format(target_path))


    
    #print(idf_design_builder.)
    #
    
    #print(TEMPLATE)
    
    print(idf_trnsys)
if __name__ == "__main__":
    main()
    