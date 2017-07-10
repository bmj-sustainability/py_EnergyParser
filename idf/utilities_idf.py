#!/usr/bin/env python
#
# EnergyParser
# Copyright (c) 2011, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import string
from random import choice
from lxml import etree

#import copy

#from utility_excelOLD import ExcelBookRead
#from UtilityXML import printXML
#from utility_pathOLD import split_up_path, get_files_by_ext_recurse

import pprint as pprint
pp = pprint.PrettyPrinter(indent=4)
pPrint = pp.pprint

log = logging.getLogger(__name__)

class loggerCritical:
    def __enter__(self):
        myLogger = logging.getLogger()
        myLogger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        myLogger = logging.getLogger()
        myLogger.setLevel("DEBUG")

#--- Utilities 
def root_node():
    """Start the XML tree with a root node
    """
    xmlVer = "0.2"
    # Root tag
    currentXML = etree.Element("EnergyPlus_XML", XML_version=xmlVer)
    # A comment
    commentXML = etree.Comment("XML Schema for EnergyPlus version 6 'IDF' files and OpenStudio version 0.3.0 'OSM' files")
    currentXML.append(commentXML)
    # Another comment
    commentXML = etree.Comment("Schema created April. 2011 by Marcus Jones")
    currentXML.append(commentXML)
    return currentXML

def force_list(item):
    """Forces item to be a list
    """    
    if not isinstance(item, list):
        return [item]
    else:
        return item

def gen_ID(length=4, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

def idStr(commentString, IDstring='BLANKID'):
    return ("{0}: {1}".format(IDstring, commentString))

def xpathRE(tree, strXpath):
    """
    This function is just an alias for the etree.xpath function,
    just to avoid having to always declare the namespace 're:'
    """
    return tree.xpath(strXpath, 
        namespaces={"re": "http://exslt.org/regular-expressions"})

def clean_newlines(string):
    """Strip newlines and any trailing/following whitespace; rejoin
    with a single space where the newlines were.
    
    Bug: This routine will completely butcher any whitespace-formatted
    text."""
    
    if not string: return ''
    lines = string.splitlines()
    return ' '.join( [line.strip() for line in lines] )
    
def delchars(str, chars):
    """Returns a string for which all occurrences of characters in
    chars have been removed."""

    # Translate demands a mapping string of 256 characters;
    # whip up a string that will leave all characters unmolested.
    identity = ''.join([chr(x) for x in range(256)])

    return str.translate(identity, chars)
## end of http://code.activestate.com/recipes/137951/ }}}

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0
    else: start += 0.0 # force it to be a float

    if inc == None:
        inc = 1.0

    count = int((end - start) / inc)
    if start + count * inc != end:
        # need to adjust the count.
        # AFAIKT, it always comes up one short.
        count += 1
    count += 1
    L = [None,] * count 
    for i in range(count):
        L[i] = start + i * inc
        
    return L


"""
Example (and doctest):

>>> for n, islast in iter_islast(range(4)):
...   if islast:
...       print "last but not least:",
...   print n
... 
0
1
2
last but not least: 3

>>> list(iter_islast(''))
[]
>>> list(iter_islast('1'))
[('1', True)]
>>> list(iter_islast('12'))
[('1', False), ('2', True)]
>>> list(iter_islast('123'))
[('1', False), ('2', False), ('3', True)]
>>>
"""

def iter_islast(iterable):
    """ iter_islast(iterable) -> generates (item, islast) pairs

    Generates pairs where the first element is an item from the iterable
    source and the second element is a boolean flag indicating if it is the
    last item in the sequence.
    """

    it = iter(iterable)
    prev = next(it)
    for item in it:
        yield prev, False
        prev = item
    yield prev, True



def OLD_applyTemplateNewStyle(IDFobj, templateDescriptions, templatesList):
    templateDescName = templateDescriptions[0]
    accrossDescZones = templateDescriptions[1]
    
    flagFound = False
    for template in templatesList:
        if templateDescName == template.ID:
            flagFound = True                
            #print templateDescName, "found"
            
            # Try to load the template into memory
            sysTemplateIdfObject = IDF.fromIdfFile(template.absolutePath)
#                try:        
#                    sysTemplateIdfObject = IDF.fromIdfFile(template.absolutePath)
#                except:
#                    raise NameError('Template {0} not found at path {1}'.format(template.ID, template.absolutePath))
#                
            # Handle each style of template                
            if template.templateStyle == "One":
                IDFobj.applyZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones)
            elif template.templateStyle == "N to N":
                IDFobj.applyZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones)
            elif template.templateStyle == "Named N to N":
                #print template.namingList
                IDFobj.applyNamedNNZoneTemplate(sysTemplateIdfObject, template.multiplyClass, template.zoneNamePointer, accrossDescZones, template)                    
            else:
                raise "Template style not correct"

    if not flagFound: 
        print(templateDescName, template.ID)
        raise NameError('Template \'{0}\' does not exist in currently loaded templates'.format(templateDescName))



def OLD_loadTemplates(templateDir):
    
    logging.debug("Loading templates from {0}".format(templateDir))
    
    #endCol = 1000
    #endRow = 1000           

    # Attach the excel COM object
    #xl = Dispatch('Excel.Application')

    # Open the input file
    #book = xl.Workbooks.Open(inputExcelPath)
    
    # Select the sheet
    #sheet = book.Sheets('Templates')

#    globalTemplatePath = sheet.Cells(1,2).Value
#    globalTemplatePath = os.path.normpath(globalTemplatePath)
    
    # Get the markers, place into a dictionary
    markerRow = 2
    markers = {}    
    for col in range(1,endCol):
        thisValue = sheet.Cells(markerRow,col).Value
        if thisValue != None:
            markers[str(thisValue)] = col -1
            #print thisValue
        #print markers
    
    # Could replace this whole section with xlrd module
    # But using COM is more fun!
    #templateArray = list()
    templatesList = list()

    # Loop through the templates
    for row in range(4,endRow):
        #thisTemplateID = sheet.Cells(row,1).Value
        # Found a template row
        if sheet.Cells(row,1).Value != None:
            # Start a list for this tempate
            #print thisTemplateID,
            # Now run over this row
            ID = sheet.Cells(row,1).Value
            relativePath = sheet.Cells(row,2).Value
            absolutePath = os.path.join(templatesFileDirStem,relativePath)
            absolutePath = os.path.normpath(absolutePath)
            templateStyle = sheet.Cells(row,3).Value
            multiplyClass = sheet.Cells(row,4).Value
            zoneNamePointer = sheet.Cells(row,5).Value
            
            namingList = list()
            for col in range(markers['Naming']+1,markers['Pointers']+1):
                thisValue = sheet.Cells(row,col).Value
                if thisValue != None:
                    namingList.append(str(thisValue))
                    
            pointerList = list()
            for col in range(markers['Pointers'],markers['End']+1):
                thisValue = sheet.Cells(row,col).Value
                if thisValue != None:
                    pointerList.append(str(thisValue))
                                   
            if templateStyle == "One":
                templatesList.append(SingularTemplate(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer))
            elif templateStyle == "N to N":
                templatesList.append(N2N_Template(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer))
            elif templateStyle == "Named N to N":
                templatesList.append(NamedN2N_Template(ID, absolutePath, templateStyle, multiplyClass,zoneNamePointer,namingList))


            #templateArray.append(templateList)
    
#    book.Close(SaveChanges=0) #to avoid prompt
#    xl.Application.Quit()

    book.Close(False)
    xl.Application.Quit()
    
    # Split up the list into seperate lists
#    for templateList in templateArray:
#        #generalList = templateList[0:markers['Naming']]
#        namingList = templateList[markers['Naming']:markers['Pointers']]
#        pointerList =  templateList[markers['Pointers']:-1]
#        #print generalList,namingList,pointerList
#        
#        templateStyle = generalList[2]
#        
#        if templateStyle == "One":
#            templatesList.append(SingularTemplate(generalList))
#        elif templateStyle == "N to N":
#            templatesList.append(N2N_Template(generalList))
#        elif templateStyle == "Named N to N":
#            templatesList.append(NamedN2N_Template(generalList,namingList,pointerList))

            
    return templatesList





def OLD_getTemplates(templatePath, filterRegExString = ".", flgExact = True):
    raise
    # Used to be a method on IDF class
    # This is just a filter for file names now...
    """Given a path, return a list of matching IDF files, and load into IDF objects
    """ 

    templates = list()
    if flgExact:
        filterRegExString= "^" + filterRegExString + "$"

    with loggerCritical():
        for path in get_files_by_ext_recurse(templatePath, "idf"):
            base=os.path.basename(path)
            fileName = os.path.splitext(base)[0]
            if  re.search(filterRegExString,fileName):
                #print path
                template=IDF.fromIdfFile(path,fileName)
                #template.getTemplateInfo()
                templates.append(template)
    
    # No duplicates!
    assert(len(templates) == len(set(templates)))
    assert len(templates)
    
#    assert(len(thisTemplate) == 1), "Template; {} found {} matches {}".format(templateDef['templateName'],
#                    len(thisTemplate),thisTemplate)
#    thisTemplate = thisTemplate[0]    
        
    
    logging.debug("Found {} templates in {} filtered {}".format(len(templates),IDF_TEMPLATE_PATH, filterRegExString))
    
    return templates


