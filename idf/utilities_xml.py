#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
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

    
def tree_get_class(IDFtree, classNameRegex, flgExact = True):
    """Returns a list of XML OBJECT nodes according to search of class name
    """
    
    #assert(isinstance(IDFtree,etree._ElementTree)), "Expected etree._Element, got {}".format(type(IDFtree))
    if flgExact:
        classNameRegex = "^" + classNameRegex + "$" 
    xpathSearch = "//CLASS[re:match(text(), '" + classNameRegex + "')]/.."
    queryElements = xpathRE(IDFtree,xpathSearch)
    queryElements = force_list(queryElements)

    logging.debug('Search of {} {} hits in {}'.format(classNameRegex, len(queryElements),IDFtree))
    
    return queryElements
    
def xpathRE(tree, strXpath):
    """
    This function is just an alias for the etree.xpath function,
    just to avoid having to always declare the namespace 're:'
    """
    return tree.xpath(strXpath, 
        namespaces={"re": "http://exslt.org/regular-expressions"})

#--- Introspection 

def get_zone_name_list(IDFobj, zoneName='.'):
    """ Return a list of zone names in the IDF object
    """
    with loggerCritical():
        zoneElements = tree_get_class(IDFobj.XML, "^Zone$")
    
    names = list()
    for zoneEl in zoneElements:
        nameXml = zoneEl.xpath('ATTR') # Select ATTR
        name = nameXml[0].text # It's the first ATTR
        names.append(name)
    
    filteredNameList = [name for name in names if re.search(zoneName, name)]
    
    return filteredNameList

def print_table(rows):
    """Pretty print a table
    """
    headers = rows.pop(0)
    alignments = rows.pop(0)
    alignments = zip(headers, alignments)
    theTable = PrettyTable(headers)
    for align in alignments:
        theTable.set_field_align(*align)
    
    for row in rows:
        theTable.add_row(row)
        
    print theTable
    
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

    for pairs in d.items():
        classType = pairs[0],
        classType = classType[0]
        classCount = pairs[1]
        aPair =  (classType,classCount)
        tableRows.append(aPair)

    return tableHeader + tableAlign + sorted(tableRows)


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
                                              mergedIDF.numObjects,
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
            print surfaceBoundaryCond
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

    #pass

def apply_change(IDFobj, IDDobj, change):
    
    with loggerCritical():
        targetSelection = tree_get_class(IDDobj.XML, change['class'], True)
        #printXML(targetSelection[0])
    assert targetSelection
    
    with loggerCritical():
        position = get_IDD_matched_position(targetSelection[0],"field",change['attr'])
        
    assert position
    
    with loggerCritical():
        targetSelection = tree_get_class(IDFobj.XML, change['class'], True)
    
    # Match the NAME
    if len(targetSelection) > 1:
        #print targetSelection
        filteredSelection = list()
        #targetSelection = list()
        
        
        
        
        
        for cl in targetSelection:
            
            # Set the name in the tree to Upper Case
            original_name = cl[1].text
            cl[1].text = original_name.upper()
            
            change["objName"] = change["objName"].upper()
            #raise
            xpathSearch = "ATTR[re:match(text(), '" + change["objName"] + "')]/.."
            
            matchedClass = xpathRE(cl,xpathSearch)
            #print matchedClass
            if matchedClass:
                filteredSelection.append(matchedClass[0])

            # Reset the name back to original
            cl[1].text = original_name

                
            #print thisClass
        #printXML(cl)
        #print xpathSearch
        targetSelection = filteredSelection          
        assert targetSelection, "Couldn't find {} - {} - {}".format(change['class'],
                                                                    change['attr'],
                                                                    change["objName"]
                                                                    )
            #printXML(cl)
        #print targetSelection
        #raise
    
    numChanges = 0
    for thisClass in targetSelection:
        targetAttr = thisClass.xpath("ATTR[{}]".format(position))
        assert targetAttr
        #printXML(targetAttr[0])
        #logging.debug(idStr("Changing {} in {}, position {}".format(change['attr'],change['class'], position).format(change),IDFobj.ID))
        
        
        targetAttr = targetAttr[0]
        if not isinstance(change['newVal'],str):
            change['newVal'] = str(change['newVal'])
        targetAttr.text = change['newVal']
        numChanges += 1
        
    
    logging.debug(idStr("Changed {} times: {} ".format(numChanges,change,),IDFobj.ID))
    
    
    return IDFobj


def apply_template(IDFobj,IDDobj,IDFtemplate,zoneNames = ".", templateName = "No name", uniqueName = None):
    """ Template is a regular IDF object
    """
    logging.debug(idStr("Processing template *** {} ***: {}".format(templateName,IDFtemplate),IDFobj.ID)) 
    
    # Loop over each class of the template
    objectCnt = 0
    
    allObjsList = IDFtemplate.XML.xpath('//OBJECT')
    
    #replacement = random.randint(0, 1000000)
    #replacement = "{}".format(replacement)
    xml_ATTR_text_replace(allObjsList, "*SYSTEM NUMBER*",  uniqueName)
    #print allObjsList
    
    #raise 
    for thisClass in IDFtemplate.XML.xpath('//CLASS'):
        
        objectParent = thisClass.xpath("..")[0]
        # Inspect the DEFINITION of this thisClass
        objectClassName =  thisClass.text
        with loggerCritical():
            classDef = tree_get_class(IDDobj.XML, objectClassName)
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
            with loggerCritical():
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
                    print "Should {} really be multiplied?".format(objectClassName)
                    print "Position: {}".format(position)
                    print "zoneName: {}".format(zoneName)
                    print "namePosition: {}".format(namePosition)
                    printXML( classDef)
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


def get_IDD_matched_position(IDDclass,label,value):
    #search = IDDclass.xpath("ATTR[@{}='{}']".format(label,value))
    #objectName = IDDclass.xpath("CLASS")
    #assert len(search) == 1, "Object {}, {} = {}, {} hits".format(objectName[0].text, label,value,len(search))
    
    #print printXML(IDDclass)
    
    #position  = IDDclass.xpath("count(./ATTR[@{}='{}']/preceding-sibling::*)".format(label,value))
    
    
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
        print "Couldn't find {}={} in {} ".format(label,value, IDDclass[0].text )
        raise
    
    return matchList[0]





def assemble_variants(variants,IDDobj):
    """
    zoneClass - This is the target class which will be multiplied
    template - this is the template IDF Object
    """
    raise Exception("SEE VARIANTS IN CENTRAL FOR RECENT")


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

def get_templates(templatePath, filterRegExString = ".", flgExact = True):
    raise
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
                template=IDF.from_IDF_file(path,fileName)
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
        
        queryElements = tree_get_class(IDFobj.XML,className)

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
    with loggerCritical():
        targetSelection = tree_get_class(IDDobj.XML, delete['class'], True)
        #printXML(targetSelection[0])
    assert targetSelection
    #"Name"
    #with loggerCritical():
    #    position = get_IDD_matched_position(targetSelection[0],"field",change['attr'])
    #    
    #assert position
    
    with loggerCritical():
        targetSelection = tree_get_class(IDFobj.XML, delete['class'], True)
    
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

def load_cariants(inputExcelPath,path_idf_base):
    
    logging.debug("Loading variants from {0}".format(inputExcelPath))
    
    # Attach the book
    book = ExcelBookRead(inputExcelPath)

    # Select the sheet
    variantsTable = book.get_table("(Variants)", startRow = 0, endRow=None, startCol=0, endCol=None)
    try:
        variantBlockLimits = [variantsTable.index(row) for row in variantsTable if row[0]]
    except:
        print(variantsTable)
        raise
    
    variants = dict()
    while len(variantBlockLimits) > 1:
        startRow = variantBlockLimits[0]
        endRow = variantBlockLimits[1]

        #print "This variant table", 
        variantBlockLimits.pop(0)
        #print variantsTable
        variantName = variantsTable[startRow][0]
        logging.debug("Working on {} table, rows {} to {}".format(variantName,startRow, endRow))
        
        if variantName in variants:
            raise Exception("Duplicate variant name {}".format(variantsTable[startRow][0]))
        
        rawTable = variantsTable[startRow:endRow]
        description = rawTable[0][2]
        
        # Process source path
        sourcePathDefinition = rawTable[0][3]
        sourcePath = path_idf_base + sourcePathDefinition
        
        # Flags
        flagIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "flag"]
        flagDefs =  [{"flag":rawTable[ind][2],
                "argument":rawTable[ind][3]}
                for ind in flagIndices]
                
        # Deletes
        deleteIndices = [rawTable.index(row) for row in rawTable if row[1].strip() == "del"]
        deleteDefs =  [{"class":rawTable[ind][2],
                "objName":rawTable[ind][3]}
                for ind in deleteIndices]
        
        # Templates
        templateIndices = [rawTable.index(row) for row in rawTable if row[1] == "tp"] 
        templateDefs =  [{"templateName":rawTable[ind][2],
                "zones":rawTable[ind][3],
                "uniqueName":"{}".format(rawTable[ind][4])} 
                for ind in templateIndices]
        # Changes
        changeIndices = [rawTable.index(row) for row in rawTable if row[1] == "ch"] 
        changeDefs = [{"class":rawTable[ind][2],
                "objName":rawTable[ind][3],
                "attr":rawTable[ind][4],
                "newVal":rawTable[ind][5],
                } 
                for ind in changeIndices]
        
              
        variants[variantName] = {
                                 "flags" : flagDefs,
                                 "deletes" : deleteDefs,
                                 "templates" : templateDefs,
                                 "changes" : changeDefs,
                                 "source" : sourcePath,
                                 "description" : description,
                                 
                                 }
    #print variants
    for var in variants:
        thisVar = variants[var]
        logging.debug("      *** {:>5} - {:<50} *** ".format("Variant",var))
        
        logging.debug("{:>20} : {:<50}".format("templates",len(thisVar["templates"])))

        logging.debug("{:>20} : {:<50}".format("flags",len(thisVar["flags"])))
                      
        logging.debug("{:>20} : {:<50}".format("deletes",len(thisVar["deletes"])))
        logging.debug("{:>20} : {:<50}".format("changes",len(thisVar["changes"])))
        logging.debug("{:>20} : {:<50}".format("description",thisVar["description"]))
        logging.debug("{:>20} : {:<50}".format("source",thisVar["source"]))

   
    #print variants
    logging.debug("Loaded {} variants from {}".format(len(variants),inputExcelPath))
    
    
    
    
    return variants

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
