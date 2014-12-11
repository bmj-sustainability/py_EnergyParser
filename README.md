Developed for complex and robust IDF pre-processing using Python and the fast c-based lxml library.

The raison d'etre of EnergyParser is to capitalize on the XML standard, a widely accepted format for attributed and hierarchical data exchange and manipulation. My personal use case has been to automate the complex generation of IDF variants based on templates and changes, for compliance with LEED energy modeling and for research simulation.

Releasing under open source GPL3.

Features:
1. Round trip parsing IDF <-> XML

2. Native regular expression support in object manipulation for complex selections

3. Full XML support through the popular 'lxml' module including EXtensible Stylesheet Language (XSLT) pipeline manipulation
4. Utility functions for common IDF operations
    - List objects
    - Selections based on class or attribute regex string search
    - Update and modify based on IDD  attribute search
    - Merge XML trees
    - Delete classes
    - Write to IDF or XML

Examples and help:
http://nbviewer.ipython.org/github/MarcusJones/EnergyParser/blob/master/Help/00%20EnergyParser-checkpoint.ipynb

Source github:
https://github.com/MarcusJones/EnergyParser


KNOWN BUGS
The latest IDD might have a single syntax error which breaks parsing, so far easiest to put a carriage return before the \choice
