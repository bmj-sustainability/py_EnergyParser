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

def gen_ID(length=4, chars=string.letters + string.digits):
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
