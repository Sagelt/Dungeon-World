#!/usr/bin/env python
# -*- coding: latin-1 -*-
import re
import sys
import os
from optparse import OptionParser

# Setup options
parser = OptionParser(usage="Usage: %prog [options] files")
parser.add_option('-s', '--safe', action="store_true", dest="safe",
	help="Instead of overwriting files, store output to a copy of each file.")
(options, args) = parser.parse_args()

# Setup general replacements to be made in the text
replacements = []

# InDesign encodes apostrophese as &apos; which isn't actually needed to re-import, so undo it
# to preserve readability
replacements.append( (re.compile(r'\&apos\;'), "'") ); 

# InDesign encodes turns smart quotes into &quot; but we just want dumb quotes for the XML.
replacements.append( (re.compile(r'\&quot\;'), "\"") );

# I'm a stickler for proper en-dash usage. Any numerical range should be an en-dash, not a
# hyphen. 
replacements.append( (re.compile(r'(?<=\d)-(?=\d)'), "–") );

# Also a stickler for em-dash usage. This catches the common internet patterns of " - "
# and " -- " and replaces them with a proper em-dash
replacements.append( (re.compile(r' -{1,2} '), "—"))
replacements.append( (re.compile(r' — '), "—"))
replacements.append( (re.compile(r' – '), "—"))

# Adam is the king of the doublespace. Get rid of it.
replacements.append( (re.compile(r'  '), " ") ) 


for filename in args:
    with open(filename, "r") as infile:
        output = []
        for line in infile:
            fixedline = line
            for replacement in replacements:
                fixedline = replacement[0].sub(replacement[1], fixedline)
            
            index = 0
            while index < len(fixedline)-2:
                if fixedline[index:index+3] == "\xE2\x80\xA9":
                    output.append("\n")
                    index += 3
                else:
                    output.append(fixedline[index])
                    index += 1
        
        outfileName = os.path.splitext(filename)[0]
        if options.safe:
            # This is a really ugly way to do this, and it isn't absolutely safe (file could 
            # already exist), but it works for now.
            outfileName += ".out"
        outfileName += os.path.splitext(filename)[1]
        
        with open(outfileName, "w") as outfile:
            outfile.write("".join(output))
    