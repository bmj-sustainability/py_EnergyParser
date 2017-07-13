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

#--- Standard
import re
import logging

#--- Utilities
from utilities_idf import idStr, root_node, gen_ID

#--- Third party
from lxml import etree

class IDF(object):
    '''
    The IDF class exists to transform a well formed ASCII .idf file into XML
    
    The class is a 'round trip' parser: 
    1. From IDF into XML \
    2. XML operations on the IDF data
    3. Write back to IDF
    The other direction is also supported
    
    The object loads data into memory
    There are multiple instantiation modes available;
     - From an IDF file
     - From a previously transformed XML file
     - A blank empty object
     
    The object has two conversion methods, from IDF -> XML and from XML -> IDF
    
    The data is therefore 'mirrored' from IDF to XML within the class
    Updating one to the other is 'automatic' or depending on your needs can be controlled direct
    
    Finally, the memory data can be written to IDF or XML
    
    Advanced utilities for processing the data are available in utilities_xml
    '''
    
    #--- Creation
    #def __init__(self, pathIdfInput=None, XML=None, IDF_string = None, pathIdfOutput = None):
    def __init__(self, pathIdfInput=None, ID = None):
        # The path to source file
        self.pathIdfInput = pathIdfInput

        # Generate a random ID
        if not ID:
            self.ID = gen_ID()
        
        # Created later
        #self.XML = None

    @classmethod
    def from_IDF_file(cls, pathIdfInput, ID = None):
        # First start a blank object
        thisClass = IDF(pathIdfInput=pathIdfInput, ID=ID)
        if not ID:
            thisClass.ID = gen_ID()
        else: 
            thisClass.ID = ID
        
        # Assign the path object
        # Call the load
        thisClass.load_IDF()
        # Call convert
        thisClass.parse_IDF_to_XML()
        # Return this class
        #print("TEST")
        logging.debug(idStr('Created an IDF object named {}, with {} objects'.format(
                                                                               thisClass.ID,
                                                                               thisClass.num_objects,
                                                                               ), thisClass.ID))
        return thisClass

    @classmethod
    def from_IDD_file(cls, pathIdfInput, ID = None):
        # First start a blank object
        thisClass = IDF(pathIdfInput=pathIdfInput, ID=ID)
        thisClass.ID = ID
        
        # Assign the path object
        # Call the load
        thisClass.load_IDF()
        # Call convert
        thisClass.parse_IDF_to_XML_2()
        # Return this class

        logging.debug(idStr('Created an IDD (DEFINITION) object named {}, with {} objects'.format(
                                                                               thisClass.ID,
                                                                               thisClass.num_objects,
                                                                               ), thisClass.ID))
        return thisClass


    @classmethod
    def from_XML_file(cls, pathXmlFile):
        # Instantiate from an xml file on disk
        
        thisClass = IDF()
        thisClass.load_XML(pathXmlFile)
        
        return thisClass
    
    @classmethod
    def from_XML_object(cls, XML):
        # Instantiate a new empty IDF object
        
        # First start a blank object
        thisClass = IDF()
         
        # Assign the XML object
        thisClass.XML = XML
        # Return this class
        #logging.debug(idStr('Created IDF object from XML object', thisClass.ID))
#        logging.debug(idStr('Created an IDF object named {}, with {} objects'.format(
#                                                                               thisClass.ID,
#                                                                               thisClass.num_objects,
#                                                                               ), thisClass.ID))
#        
        return thisClass

    #--- Introspection
    #--- Introspection
    
    def __str__(self):
        return "IDF:{}, IDF Lines:{}, XML Objects:{}, XML_root:{}".format(
                             self.ID,
                             self.num_lines,
                             self.num_objects,
                             self.XML,
                             )
            #'Loaded IDF {0} with {1} lines'.format(self.pathIdfInput,countLines),
            #sxself.ID))
    
    @property
    def num_lines(self):
        try: 
            #self.IDF_string
            return(len(self.IDF_string.split('\n')))
        except:
            return 0
    
    @property
    def num_objects(self):
        if self.XML is not None:
            objects = self.XML.xpath('OBJECT')
            return(int(len(objects)))
        else:
            return 0 

    def print_template_def(self):
        try:
            print(self.templateDef)
        except:
            raise Exception("Template not defined")
    
    def list_classes(self):
        if self.XML is not None:
            objects = self.XML.xpath('OBJECT')
            return(objects)
        else:
            return 0 
        

    #--- Load data
    def load_XML(self, XMLpath):
        # Load XML from file on disk
        self.XML = etree.parse(XMLpath)
        
        logging.debug(idStr(
            'Loaded XML from {}, {} objects'.format(
                                                 XMLpath, self.num_objects
                                                 ),self.ID))

    def load_IDF(self):
        # Load IDF file lines into memory 
        
        # Define input and output full file paths
        fIn = open(self.pathIdfInput, 'r')
       
        self.IDF_string = fIn.read()
        
        countLines = 0
        for line in self.IDF_string.split('\n'):
            countLines += 1

        logging.debug(idStr(
            'Loaded IDF {} with {} lines'.format(
                                                 self.pathIdfInput,
                                                 countLines,
                                                 ),self.ID))
        
        fIn.close()
        
    #--- Convert data

    def convert_XML_to_IDF(self):
        # This method uses XSLT transform to convert XML into the IDF
        
        stringTransform = """<?xml version="1.0" ?>
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:output method="text" indent="no"/>
            
            <xsl:template match="EnergyPlus_XML">
            <ROOT>
            <!-- New line, and select all OBJECTS -->
            <xsl:text>&#xa;</xsl:text>
            <xsl:apply-templates select="OBJECT"/>
            </ROOT>
            
            </xsl:template>
            
            <xsl:template match="OBJECT">
                <!-- Select NAME and newline -->
                <xsl:apply-templates select="CLASS"/>
                <xsl:text>&#xa;</xsl:text>
                <!-- Then select ATTR and newline -->
                <xsl:apply-templates select="ATTR"/>
                <xsl:text>&#xa;</xsl:text>
            </xsl:template>
            
            <!-- Write the class name and a comma -->
            <xsl:template match="CLASS"><xsl:value-of select="." />
                <xsl:text>,</xsl:text>
                <!-- Tab, !, and comment -->
                <xsl:text>&#9;</xsl:text>    
                <xsl:text>!</xsl:text>
                <xsl:value-of select="@Comment"/>
            </xsl:template>
            
                
            <!-- Add a tab, then attribute -->
            <xsl:template match="ATTR"><xsl:text>&#9;</xsl:text><xsl:value-of select="." />
                
                <!-- Add either a comma or a semi colon -->
                <xsl:if test="position() != last()">
                    <xsl:text>,</xsl:text>
                </xsl:if>
                <xsl:if test="position() = last()">
                    <xsl:text>;</xsl:text>
                </xsl:if>
                
                <!-- Tab, !, and comment -->
                <xsl:text>&#9;</xsl:text>    
                <xsl:text>!</xsl:text>
                <xsl:value-of select="@Comment"/>
                
                <!-- New line -->
                <xsl:text>&#xa;</xsl:text>
            </xsl:template>
            
            </xsl:stylesheet>
            """
        
        # Load the XSLT string into an etree
        xmlTransformXML = etree.XML(stringTransform)
        
        # Convert the XML into an XSLT transform object
        transform = etree.XSLT(xmlTransformXML)
        
        # Write a new IDF file from the current XML
        newIdfXml = transform(self.XML)
     
        self.IDF_string = newIdfXml.__str__()
        
        logging.debug(idStr(
            'Converted XML to IDF, {} objects'.format(self.num_objects),
            self.ID))
        

    def tokenize(self,thisLine):
        tokens = dict()
        
#         splitDict = {
#              "splitFld"                 : re.compile(r"\\ \w+",re.VERBOSE),
#              "splitComma"   : re.compile(r",",re.VERBOSE),
#                  }
#         
        pattDict = {
                    "Object"          : re.compile(r"^\s*[\w:]+\s*[,;]",re.VERBOSE),
                    "Field"                 : re.compile(r"\\ \S+",re.VERBOSE),
                    "splitSemi"   : re.compile(r";",re.VERBOSE),
                    
                    }    
        
        # Check for field, strip it off
        if re.search(pattDict["Field"], thisLine):
            
            thisLine = str(thisLine.encode('utf-8').decode('ascii', 'ignore'))
            # Get field name
            fieldNameToken = re.findall(pattDict["Field"],thisLine)
            
            assert len(fieldNameToken) == 1, Exception("ERROR on this line\n {}".format(thisLine))
            
            fieldNameFirst = fieldNameToken[0][1:]
            fieldNameFirst=re.sub(r">","_GT",fieldNameFirst)
            fieldNameFirst=re.sub(r"<","_LT",fieldNameFirst)
            fieldNameFirst=re.sub(r":","_",fieldNameFirst)

            tokens["fldName"] = fieldNameFirst
            
            # Split the line on the field
            splitLine = re.split(pattDict["Field"],thisLine)
            assert len(splitLine) == 2
            # Left side is the new line to process
            thisLine = splitLine[0]  
            # Right side is the field text
            tokens["fldText"] = splitLine[1].strip()
            
        # Check for object(s)
        if re.search(pattDict["Object"], thisLine):
            if re.search(pattDict["splitSemi"], thisLine):
                # This signals the end of an object
                tokens["flgEnd"] = True
                
            # Found at least one object
            # Split the line on the seperators
            splitLine = re.split(r"[,;]", thisLine)
            if type(splitLine) is  not list: 
            #instance(splitLine, str):
                splitLine = [splitLine]
            
            
            attribs = list()
            attribs = attribs + [attrib for attrib in splitLine if re.search("\S+",attrib)]
            if attribs:
                tokens["attribs"] = [attrib.strip() for attrib in attribs]

            
        return tokens
    
    def parse_IDF_to_XML_2(self):
        """Currently used for IDD object, but potentially used for IDF
        """
        currentXML = root_node()
        
        pattDict = {
                    "Comment line"          : re.compile(r"^!",re.VERBOSE),
                    "Blank"                 : re.compile(r"^\s*$",re.VERBOSE),
                    "EmptyGroup"            : re.compile(r"^\s* [\S \s]+ ;$",re.VERBOSE),
#                    "Start Object"          : re.compile(r"[,;]$",re.VERBOSE),
#                    "Inside Object"         : re.compile(r",",re.VERBOSE),                    
#                    "End Object"            : re.compile(r";",re.VERBOSE),
#                    "Field"                 : re.compile(r"\\ \S+",re.VERBOSE),
#                    
                    }
        
        lines = list()
        for line in self.IDF_string.split('\n'):
            lines.append(line)   
        
        lineIndex = 0 
        
        flgObject = False
        
        
        while (lineIndex < len(lines)) :
            thisLine = lines[lineIndex]
            #print thisLine
            
            # Skip
            if re.search(pattDict["Comment line"], thisLine):
                pass
            # Skip
            elif re.search(pattDict["Blank"], thisLine):
                pass
            elif re.search(pattDict["EmptyGroup"], thisLine):
                pass
                        
            else:
                tokens = self.tokenize(thisLine)
                if "attribs" in tokens:
                    if (flgObject==False):
                        #print "Start",
                        flgObject = True
                        thisObjectXML = etree.SubElement(currentXML, "OBJECT")
                        
                        for attrib in tokens["attribs"]:
                            tokens["attribs"].remove(attrib)
                            thisATTRXML = etree.SubElement(thisObjectXML, "CLASS")
                            thisATTRXML.text = attrib
                            
                    if (flgObject==True):
                        for attrib in tokens["attribs"]:
                            tokens["attribs"].remove(attrib)
                            thisATTRXML = etree.SubElement(thisObjectXML, "ATTR")
                            thisATTRXML.text = attrib
                            
                if "fldName" in tokens and flgObject:
                    #print tokens["fldName"],
                    #thisATTRXML[tokens["fldName"]] = tokens["fldText"]
                    if thisATTRXML.get(tokens["fldName"]):
                        oldText = thisATTRXML.get(tokens["fldName"])
                        newText = oldText +" " + tokens["fldText"]
                        thisATTRXML.set(tokens["fldName"], newText)
                    else:
                        try:
                            thisATTRXML.set(tokens["fldName"], tokens["fldText"])
                        except:
                            print(tokens)
                            raise
                    
                if "flgEnd" in tokens:
                    flgObject = False
                    #print "End",                    
                    
                if "fldName" in tokens and not flgObject:                    
                    try:
                        thisATTRXML.set(tokens["fldName"], tokens["fldText"])
                    except:
                        pass
                    

                #print "{:50} {:30}".format(tokens, thisLine)
                
                
                
                
            lineIndex += 1
        
        #print currentXML.text
        
        self.XML = currentXML

        logging.debug(idStr(
            'Converted IDD to XML:{} {}, {} objects'.format( 
                                                       type(self.XML),
                                                       self.XML,
                                                       self.num_objects,
                                                       ),self.ID))    
    def parse_IDF_to_XML(self):
        
        #=======================================================================
        # This is the updated version, with the capability to handle OSM files!
        #=======================================================================
        
        
        
         # create a local copy
        lines = []
        
        for line in self.IDF_string.split('\n'):
            lines.append(line)

        currentXML = root_node()
        lineIndex = 0
        #zoneNameIndex = 0
        
        #print len(lines)
        
        flagStart = False
        flagEnd = False
        
        
        # Loop over each line
        while (lineIndex < len(lines)) :
            
            thisLine = lines[lineIndex]
            
            # Strip the comment
            comment = "No comment"
            # ANOTHER HACK! Just blanking a full comment line, handled later in scipt!
            if re.search(r"^!", thisLine,re.VERBOSE):
                #print "SKIP"
                thisLine = ""     
            elif re.search(r"!", thisLine,re.VERBOSE):
                # Update to only split ONCE
                try: 
                    values,comment = re.split(r"!", thisLine,re.VERBOSE, 1)
                except:
                    print(re.split(r"!", thisLine,re.VERBOSE))
                    raise Exception("Maybe a line with 2 ! ? Try to catch these before")
                comment = comment.rstrip()
                comment = comment.lstrip()                
                #print values
                thisLine = values
            # And strip any white space
            thisLine = thisLine.rstrip()
            thisLine = thisLine.lstrip()

            
            #print thisLine
            
            # If it has no , or ;, completely skip the line
            # Otherwise do this:
            if re.search(r"[,;]", thisLine,re.VERBOSE):
                
                #print "2"
                #print thisLine
                
                # This is a HACK
                appendThis = ""
                if re.search(r";", thisLine,re.VERBOSE):
                    appendThis = ";"
                
                items = re.split(r"[,;]", thisLine,re.VERBOSE)
                
                #print items
                # re.split annoyingly returns an extra entry at the end 
                # REMOVE IT
                items = items[0:-1]
                #print items
                
                # More HACK
                items[-1] = items[-1] + appendThis
                #print items
                
                for item in items:
                    item.rstrip()
                    item.lstrip()
                    
                    if not item and not flagStart:
                        #print ""
                        raise "Blank - Should NEVER see thsi!"

                    # Found a ;, END
                    # Create an ATTR
                    elif re.search(r";", item,re.VERBOSE) and flagStart: 
                        flagStart = False
                        #print "END", item
                        item = item.replace(r";","")
                        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
                        thisAttrXML.text = item
                        thisAttrXML.set("Comment", comment)
                        
                    
                    # Found a START
                    # Create a CLASS
                    elif not flagStart:
                        flagStart = True
                        #print "START", item
    
                        # Start an Object
                        thisObjectXML = etree.SubElement(currentXML, "OBJECT")
                        # An object always has a Class
                        thisClassXML = etree.SubElement(thisObjectXML, "CLASS")
                        thisClassXML.text = item
                    
                    # Found a INSIDE
                    # Create an ATTR         
                    elif flagStart: 
                        #print "INSIDE", item
                        thisAttrXML = etree.SubElement(thisObjectXML, "ATTR")
                        thisAttrXML.text = item
                        thisAttrXML.set("Comment", comment)
                        
    
                 
            lineIndex += 1
            # END WHILE 
        # END IF
        
        # The XML is saved
        self.XML = currentXML

        logging.debug(idStr(
            'Converted IDF to XML:{} {}, {} objects'.format( 
                                                       type(self.XML),
                                                       self.XML,
                                                       self.num_objects,
                                                       ),self.ID))
    #--- Write data
    def write_IDF(self, pathIdfOutput):
        
        # Ensure conversion to XML
        self.convert_XML_to_IDF()
        
        self.pathIdfOutput = pathIdfOutput
        
        #XMLstring = (etree.tostring(self.XML, pretty_print=True))
        
        
        #if not os.path.exists(pathIdfOutput):
        #    os.makedirs(pathIdfOutput)

        fOut = open(self.pathIdfOutput, 'w')
        
        fOut.write(self.IDF_string)
        
        fOut.close()

        logging.debug(idStr(
            'Wrote IDF {}, {} objects'.format(pathIdfOutput,self.num_objects, self.num_lines),
            self.ID))
        
    def write_XML(self,pathXmlOutput):

        self.pathXmlOutput = pathXmlOutput

        fOut = open(self.pathXmlOutput, 'w')

        resultXML = (etree.tostring(self.XML, pretty_print=True))

        fOut.write(resultXML)
        fOut.close
        
        #pathIdfOutput
        
        logging.debug(idStr(
            'Wrote XML {0}'.format(self.pathXmlOutput),
            self.ID))

    #--- Utility
    def __add__(self,other):
        return merge_xml(self, other)




    
