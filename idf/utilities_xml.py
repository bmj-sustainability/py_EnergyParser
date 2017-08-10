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

#===============================================================================
# Set up
#===============================================================================




#--- Standard library
import re
from collections import defaultdict # Python 2.7 has a better 'Counter'
from copy import deepcopy
import os

#--- Utilities
#from utility_print_table import PrettyTable
from utility_logger import LoggerCritical
from utilities_idf import force_list, xpathRE, clean_newlines, root_node, idStr

#--- Third party
from lxml import etree

#--- Mine
from idf_parser import IDF



#===============================================================================
# Logging
#===============================================================================
import logging
#logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#--- XML Utilities

def xml_ATTR_text_replace(objects, searchStr, theNewText):
    """Given a list of XML node objects, search through all ATTR elements
    Replace the "placeHolder" string with "theNewText"
    Returns the entire XML node
    """
    assert isinstance(objects,list)
    replaceCnt = 0
    for obj in objects:
        #print obj
        for attr in obj.xpath("ATTR"):
            # Replace all searchStr!
            #print attr
            if re.search(re.escape(searchStr), attr.text):
                attr.text = re.sub(re.escape(searchStr), theNewText, attr.text)
                replaceCnt = replaceCnt + 1
    logging.debug("Replaced {} with {}, {} times".format(searchStr,theNewText,replaceCnt))
    

def get_ATTR_position(IDDobj, className, XMLattribName, XMLattribValue):
    """Given an IDD object, search for a class, an attribute, and it's value, return the
    position
    """
    classDef = tree_get_class(IDDobj.XML, className)
    assert len(classDef) == 1, "Actual length {}".format(len(classDef))
    classDef = classDef[0]
    
    position = classDef.xpath("count(./ATTR[@{}='{}']/preceding-sibling::*)+1".format(XMLattribName, XMLattribValue))
    
    return position

def tree_get_class(idf_obj, classNameRegex, flgExact = True):
    """Returns a list of XML OBJECT nodes according to search of class name
    """
    
    IDFtree = idf_obj.XML
    #assert(isinstance(IDFtree,etree._ElementTree)), "Expected etree._Element, got {}".format(type(IDFtree))
    if flgExact:
        classNameRegex = "^" + classNameRegex + "$" 
    xpathSearch = "//CLASS[re:match(text(), '" + classNameRegex + "')]/.."
    queryElements = xpathRE(IDFtree,xpathSearch)
    queryElements = force_list(queryElements)
    
    logging.debug('Search of {} {} hits in {}'.format(classNameRegex, len(queryElements),IDFtree))
    
    return queryElements
#--- Printing

def get_table_all_names(IDFobj):
    """Lists all objects, and their names (first ATTR)
    """
    objects = IDFobj.XML.xpath('//OBJECT')
    
    tableHeader = [("Class", "Name")]
    tableAlign = [("r", "l")]
    tableRows = list()
    for object in objects:
        # Select the class of each object
        type = object.xpath('CLASS')
        name = object.xpath('ATTR')
        tableRows.append((type[0].text, name[0].text))

    return tableHeader + tableAlign + sorted(tableRows)


def get_table_object_count(IDFobj):
    
    names = IDFobj.XML.xpath('//CLASS')
    
    L = [name.text for name in names]

    d = defaultdict(int)
    for i in L:
        d[i] += 1
    
    tableHeader = [("Class", "Count")]
    tableAlign = [("r", "l")]
    tableRows = list()

    for pairs in list(d.items()):
        classType = pairs[0],
        classType = classType[0]
        classCount = pairs[1]
        aPair =  (classType,classCount)
        tableRows.append(aPair)

    return tableHeader + tableAlign + sorted(tableRows)


def print_table(rows, num_rows=None):
    """Pretty print a table
    """
    raise
    headers = rows.pop(0)
    alignments = rows.pop(0)
    alignments = list(zip(headers, alignments))
    theTable = PrettyTable(headers)
    for align in alignments:
        theTable.set_field_align(*align)
    if num_rows:
        for row in rows[0:num_rows]:
            theTable.add_row(row)
    else:
        for row in rows:
            theTable.add_row(row)        
    print(theTable)
    

## {{{ http://code.activestate.com/recipes/137951/ (r1)
def printDict(di, fmt="%-25s %s"):
    for (key, val) in list(di.items()):
        print(fmt % (str(key)+':', val))


def prettyPrintCols(strings, widths, split=' '):
    """Pretty prints text in colums, with each string breaking at
    split according to prettyPrint.  margins gives the corresponding
    right breaking point."""

    assert len(strings) == len(widths)

    strings = list(map(clean_newlines, strings))

    # pretty print each column
    cols = [''] * len(strings)
    for i in range(len(strings)):
        cols[i] = prettyPrint(strings[i], widths[i], split)

    # prepare a format line
    format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"

    def formatline(*cols):
        return format % tuple([(s or '') for s in cols])

    # generate the formatted text
    return '\n'.join(map(formatline, *cols))

def printXML(theXMLtree):
    print(etree.tostring(theXMLtree, pretty_print=True))

def prettyPrint(string, maxlen=75, split=' '):
    """Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split
    is found"""

    # Tack on the splitting character to guarantee a final match
    string += split
    
    lines   = []
    oldeol  = 0
    eol     = 0
    while not (eol == -1 or eol == len(string)-1):
        eol = string.rfind(split, oldeol, oldeol+maxlen+len(split))
        lines.append(string[oldeol:eol])
        oldeol = eol + len(split)

    return lines


#--- Introspection 
def get_zone_name_list(IDFobj, zoneName='.'):
    """ Return a list of zone names in the IDF object
    """
    with LoggerCritical():
        zoneElements = tree_get_class(IDFobj, "^Zone$")
    
    names = list()
    for zoneEl in zoneElements:
        nameXml = zoneEl.xpath('ATTR') # Select ATTR
        name = nameXml[0].text # It's the first ATTR
        names.append(name)
    
    filteredNameList = [name for name in names if re.search(zoneName, name)]
    
    return filteredNameList



#--- Assembly


#--- Manipulate Objects / CONFIRMED
def merge_xml(objectA, objectB):
    """Given 2 XML nodes, return a merged tree composed of the 2
    """
    # Start a new XML root object
    currentXML = root_node()

    # Create the new IDF object with this root
    mergedIDF = IDF.from_XML_object(currentXML)

    AObjects = objectA.XML.xpath('//OBJECT')
    for object in AObjects:
        mergedIDF.XML.append(object)

    BObjects = objectB.XML.xpath('//OBJECT')
    for object in BObjects:
        mergedIDF.XML.append(object)
    
    logging.debug(idStr(
        "'{}':{} + '{}':{}  = '{}':{} Union operation".format(
                                                  objectA.ID,
                                              int(len(AObjects)), 
                                              objectB.ID,
                                              int(len(BObjects)),
                                              mergedIDF.ID,
                                              mergedIDF.num_objects,
                                              ),
        mergedIDF.ID))
    
    return mergedIDF


def apply_default_construction_names(IDFobj, IDDobj):
    
    
    xpathSearch = r"OBJECT/CLASS[text() = 'BuildingSurface:Detailed']/.."
    surfaceObjs = IDFobj.XML.xpath(xpathSearch)
    for surface in surfaceObjs: 
        
        surfaceType = surface.xpath("ATTR[2]")[0].text
        surfaceBoundaryCond = surface.xpath("ATTR[5]")[0].text
        surfaceConstructionName = surface.xpath("ATTR[3]")[0]
        if surfaceBoundaryCond == "Surface":
            if surfaceType == "Ceiling":
                surfaceConstructionName.text = "Interior Ceiling"
            elif surfaceType == "Wall":
                surfaceConstructionName.text = "Interior Wall"
            elif surfaceType == "Floor":
                surfaceConstructionName.text = "Interior Floor"
            else:
                raise            
        elif surfaceBoundaryCond == "Outdoors" or surfaceBoundaryCond == "Adiabatic":
            if surfaceType == "Ceiling" or surfaceType == "Roof":
                surfaceConstructionName.text = "Exterior Roof"
            elif surfaceType == "Wall":
                surfaceConstructionName.text = "Exterior Wall"
            elif surfaceType == "Floor":
                surfaceConstructionName.text = "Exterior Floor"
            else:
                raise Exception("Surface type not found {}".format(surfaceType))
            
        elif surfaceBoundaryCond == "Ground":
            surfaceConstructionName.text = "Exterior Floor"
            
        else:
            print(surfaceBoundaryCond)
            raise
        
    logging.debug(idStr("Applied dummy constructions to {} surfaces".format(len(surfaceObjs)),IDFobj.ID))
        
    xpathSearch = r"OBJECT/CLASS[text() = 'FenestrationSurface:Detailed']/.."
    surfaceObjs = IDFobj.XML.xpath(xpathSearch)
    for surface in surfaceObjs: 
        surfaceType = surface.xpath("ATTR[2]")[0].text
        surfaceBoundaryCond = surface.xpath("ATTR[5]")[0].text
        surfaceConstructionName = surface.xpath("ATTR[3]")[0]
        surfaceConstructionName.text = r"Exterior Window"
        #print surface.xpath("ATTR[3]")[0].text
    #xpathSearch = r"OBJECT/CLASS[text() = 'BuildingSurface:Detailed']/.."
    #surfaceObjs = IDFobj.XML.xpath(xpathSearch)[0]
    #printXML(surfaceObjs)
    #raise 
    #raise
    logging.debug(idStr("Applied dummy constructions to {} windows".format(len(surfaceObjs)),IDFobj.ID))


def apply_change(IDFobj, IDDobj, change):
    with LoggerCritical():
        targetSelection = tree_get_class(IDDobj, change['class'], False)
    assert targetSelection
    
    with LoggerCritical():
        position = get_IDD_matched_position(targetSelection[0],"field",change['attr'])
    assert position
    
    with LoggerCritical():
        targetSelection = tree_get_class(IDFobj, change['class'], False)
    
    # Match the NAME
    if len(targetSelection) > 1:
        filteredSelection = list()
        
        for cl in targetSelection:
            
            # Set the name in the tree to Upper Case
            original_name = cl[1].text
            cl[1].text = original_name.upper()
            
            change["objName"] = change["objName"].upper()
            #raise
            xpathSearch = "ATTR[re:match(text(), '" + change["objName"] + "')]/.."
            
            matchedClass = xpathRE(cl,xpathSearch)
            if matchedClass:
                filteredSelection.append(matchedClass[0])

            # Reset the name back to original
            cl[1].text = original_name

        targetSelection = filteredSelection          
        assert targetSelection, "Couldn't find {} - {} - {}".format(change['class'],
                                                                    change['attr'],
                                                                    change["objName"]
                                                                    )
    
    numChanges = 0
    for thisClass in targetSelection:
        targetAttr = thisClass.xpath("ATTR[{}]".format(position))
        assert targetAttr
        
        targetAttr = targetAttr[0]
        if not isinstance(change['newVal'],str):
            change['newVal'] = str(change['newVal'])
        targetAttr.text = change['newVal']
        numChanges += 1
        
    
    logging.debug(idStr("Applied change {} times: \n{} ".format(numChanges,change,),IDFobj.ID))
    
    return IDFobj


def apply_template(IDFobj,IDDobj,IDFtemplate,zoneNames = ".", templateName = "No name", uniqueName = None):
    """ Template is a regular IDF object
    """
    logging.debug(idStr("Processing template *** {} ***: {}".format(templateName,IDFtemplate),IDFobj.ID)) 
    
    #TODO: For some reason, the template IDF object is losing it's XML parse, so it has to be re-parsed!
    IDFtemplate.parse_IDF_to_XML()
    #print(IDFtemplate)
    
    
    # Loop over each class of the template
    objectCnt = 0
    
    allObjsList = IDFtemplate.XML.xpath('//OBJECT')
    
    #replacement = random.randint(0, 1000000)
    #replacement = "{}".format(replacement)
    #xml_ATTR_text_replace(allObjsList, "*SYSTEM NUMBER*",  uniqueName)
    #print allObjsList
    
    #raise 
    for thisClass in IDFtemplate.XML.xpath('//CLASS'):
        
        objectParent = thisClass.xpath("..")[0]
        # Inspect the DEFINITION of this thisClass
        objectClassName =  thisClass.text
        with LoggerCritical():
            classDef = tree_get_class(IDDobj, objectClassName)
        assert len(classDef) >= 1, "Couldn't any {} in IDD".format(objectClassName)
        assert len(classDef) == 1, "Found {} in IDD {} times".format(objectClassName,len(classDef))
        classDef = classDef[0]

        # This thisClass is multiplied over zones! 
        if (
            (
             flag_IDD_match_field(classDef,"object-list","ZoneNames") 
             or 
             flag_IDD_match_field(classDef,"object-list","ZoneAndZoneListNames")
             ) 
                and   
            (
             flag_IDD_match_field(classDef,"field","Zone Name")
             or
             flag_IDD_match_field(classDef,"field","Zone or ZoneList Name") 
             )
            
            and
            (objectClassName not in ("Pump:VariableSpeed","WaterUse:Equipment"))
            ):
            # Get the position of the zone name
            
            #print objectClassName, 
            #(objectClassName not in ["Pump:VariableSpeed",])
            
            #raise 
            
            #raise
            with LoggerCritical():
                try:
                    position = get_IDD_matched_position(classDef,"object-list","ZoneNames")
                except:
                    position = get_IDD_matched_position(classDef,"object-list","ZoneAndZoneListNames")

            #print position
            if flag_IDD_match_field(classDef,"field","Name"):
                # Get the position of the zone name
                with loggerCritical():
                    namePosition = get_IDD_matched_position(classDef,"field","Name")
            else:
                namePosition = -1
            #print flag_IDD_match_field(classDef,"field","Name")
            #print namePosition
            #raise
            # Loop over zones            
            for zoneName in get_zone_name_list(IDFobj,zoneNames):
                #print zoneName
                thisMultiplyObject = deepcopy(objectParent)
                
                if namePosition != -1:
                    uniqueNameAttr = thisMultiplyObject.xpath("//ATTR[{}]".format(int(namePosition)))
                    uniqueNameAttr[0].text = uniqueNameAttr[0].text + zoneName
                #print namePosition
                #xml_ATTR_text_replace([thisMultiplyObject], r"\*ZONENAME\*",zoneName)
                
                # Update pointer to zone name
                targetNameAttr = thisMultiplyObject.xpath("//ATTR[{}]".format(int(position)))
                #printXML(targetNameAttr[0])
                try:
                    targetNameAttr[0].text = zoneName
                except:
                    print("Should {} really be multiplied?".format(objectClassName))
                    print("Position: {}".format(position))
                    print("zoneName: {}".format(zoneName))
                    print("namePosition: {}".format(namePosition))
                    printXML(classDef)
                    raise
                #print targetNameAttr[0].text
                #printXML(thisMultiplyObject)
                IDFobj.XML.append(thisMultiplyObject)
                #logging.debug(idStr("Zonename updated, position {}".format(int(position)),IDFobj.ID))

            logging.debug(idStr("\tMerged {} into {} over {} zones matching '{}'".format(objectClassName, IDFobj.ID, len(get_zone_name_list(IDFobj)),zoneNames),IDFobj.ID))

        # Otherwise, just merge_xml it straight in
        else:
            
            # BUT: Check for any possible unique names
            IDFobj.XML.append(objectParent)
            objectCnt += 1
            
    logging.debug(idStr("\tMerged {} static objects from {}".format(objectCnt, templateName, IDFobj.ID,),IDFobj.ID)) 
    return IDFobj



def flag_IDD_match_field(IDDclass, label, value):
    #printXML(IDDclass)
    #print IDDclass.xpath("//ATTR[@{}='{}']".format(label,value))
    
    #logging.debug("{}".format(IDDclass) )
    
    if IDDclass.xpath("ATTR[@{}='{}']".format(label,value)):
        return True
    else:
        return False

def flg_IDD_has_field(IDDclass, label):
    if IDDclass.xpath("ATTR[@{}]".format(label)):
        return True
    else:
        return False 


def get_IDD_matched_position(IDDclass, label, value):
    """Given the IDD class object, return the integer position of the attribue
    """
    
    matchList = list()
    for attrMatch in IDDclass.xpath("./ATTR[@{}='{}']".format(label,value)):
        thePosition = attrMatch.xpath("count(preceding-sibling::ATTR)")
        matchList.append(int(thePosition)+1)
        
    #allMatches = 
    #print allMatches
    #print allMatches[0].xpath("count(preceding-sibling::ATTR)")
    #print IDDclass.xpath("./ATTR[@{}='{}']/preceding-sibling::ATTR)".format(label,value))[0]
    #print position
    
    #print matchList
    #raise

    logging.debug("{} {}={} positions {}".format(IDDclass,label,value,matchList))
     
    #assert matchList, 
    try:
        matchList[0]
    except:
        #print logging.debug("Couldn't find {}={} in {}".format(label,value, IDDclass))
        #printXML(IDDclass)
        #raise Exception()
        print("Couldn't find {}={} in {} ".format(label,value, IDDclass[0].text ))
        raise
    
    return matchList[0]

def get_template_path(templatePath, filterRegExString = ".", flgExact = True):
    if flgExact:
        filterRegExString= "^" + filterRegExString + "$"
        
    for root, dirs, files in os.walk(templatePath):
        for name in files:
            splitName = os.path.splitext(name)
            if splitName[1] == ".idf":
                if re.search(filterRegExString,splitName[0]):
                    return os.path.join(root, name)
#    raise
#
#    for path in get_files_by_ext_recurse(templatePath, "idf"):
#            base=os.path.basename(path)
#            fileName = os.path.splitext(base)[0]
#            if  re.search(filterRegExString,fileName):
#                #print path
#                #templatePath=IDF.from_IDF_file(path,fileName)
#                print os.path.abspath(fileName)
#                print fileName
#                raise
#                return fileName
#                ##template.getTemplateInfo()
#                #templates.append(template)
#                
    raise Exception("Template {} not found in {}".format(filterRegExString,templatePath))



def clean_out_object(IDFobj,keptClassNames, flgExact = True):
    objectTable = get_table_object_count(IDFobj)
    
    #print objectTable
    objectTable.pop(0) # Eject the header
    currentClasses = set([item[0] for item in objectTable])
    # List comprehension to create set
    deletedClasses = currentClasses - set(keptClassNames)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("CRITICAL")
    
    IDFobj = delete_classes(IDFobj,list(deletedClasses),flgExact)
    
    myLogger.setLevel("DEBUG")
    
    
    logging.debug(idStr(
        "Out of {0} classes in this IDF, {1} are deleted".format(
           len(currentClasses),
           len(deletedClasses),
           len(keptClassNames),
           ),IDFobj.ID))   
    return IDFobj


def delete_classes(IDFobj, classNames, flgExact = True):

    for className in classNames:
        className = "^" + className + "$"
        
        queryElements = tree_get_class(IDFobj,className)

        for object in queryElements:
            IDFobj.XML.remove(object)

        logging.debug(idStr(
            'Deleted {0} {1} objects'.format(len(queryElements), className),
            IDFobj.ID))
    return IDFobj


def delete_classes_from_excel(IDFobj, IDDobj, delete):
    
    logging.debug(idStr("Deleting: {}".format(delete),IDFobj.ID))
    #[{'class': u'TestClass', 'Name': u'TestName'}]
    #raise
    with LoggerCritical():
        targetSelection = tree_get_class(IDDobj, delete['class'], True)
        #printXML(targetSelection[0])
    assert targetSelection
    #"Name"
    #with loggerCritical():
    #    position = get_IDD_matched_position(targetSelection[0],"field",change['attr'])
    #    
    #assert position
    
    with LoggerCritical():
        targetSelection = tree_get_class(IDFobj, delete['class'], True)
    
    # Match the NAME
    if len(targetSelection) > 1:
        #print targetSelection
        filteredSelection = list()
        #targetSelection = list()
        for cl in targetSelection:
            xpathSearch = "ATTR[re:match(text(), '" + delete["objName"] + "')]/.."
            
            matchedClass = xpathRE(cl,xpathSearch)
            #print matchedClass
            if matchedClass:
                filteredSelection.append(matchedClass[0])
            #print thisClass
        #printXML(cl)
        #print xpathSearch
        targetSelection = filteredSelection          
        assert targetSelection, "No {}".format(delete['class'])
            #printXML(cl)
        #print targetSelection
        #raise
    
    for object in targetSelection:
        IDFobj.XML.remove(object)    

    logging.debug(idStr("Deleted: {} objects".format(len(targetSelection)),IDFobj.ID))


def short_string(theStr, length = 30):
    if len(theStr)<=length:
        return theStr
    else:
        return theStr[0:length-3] + "..."

def delete_orphaned_zones(IDFobj):

    ### GET SPACES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:Space$')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    spaces = xpathRE(IDFobj.XML,xpathSearch)
    logging.debug("Found {} OS:Space".format(len(spaces)))

    
    ### GET ZONES ###
    xpathSearch = "//CLASS[re:match(text(), '^OS:ThermalZone')]/.."
    #xpathSearch = "//OBJECT/CLASS[re:match(text(), '" + className + "')]/"
    zones = xpathRE(IDFobj.XML,xpathSearch)
    logging.debug("Found {} OS:ThermalZone".format(len(zones)))
        
    
    ### LOOP Both REVERSE ###
    notFound = 0
    for zone in zones:    
        zoneName = zone.xpath("ATTR")[0].text
        found = False
        for space in spaces:    
        
            thisSpaceName = space.xpath("ATTR")[0].text
            thisSpacePointsToZoneName = space.xpath("ATTR")[9].text                    
            #zoneName = zone.xpath("ATTR")[0].text
            if re.search("^"+zoneName+"$",thisSpacePointsToZoneName):
                #print 
                #print "Match"
                #print "Space: {}, Space points to {}, Zone exists here: {}".format(thisSpaceName,thisSpacePointsToZoneName,zoneName)
                #newZoneName =  "ZONE " + thisSpaceName
                
                #print "New name:" + newZoneName
                found = True
                #space.xpath("ATTR")[9].text = newZoneName
                #zone.xpath("ATTR")[0].text =  newZoneName
        if not found:
                IDFobj.XML.remove(zone)
                notFound += 1
            
    logging.debug("Checked {} zones over {} spaces, deleted {} zones.".format(len(zones),len(spaces),notFound))
