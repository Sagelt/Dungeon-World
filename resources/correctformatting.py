#!/usr/bin/env python
# -*- coding: latin-1 -*-
import re
import sys
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
	infile = open(filename, "r")
	output = []
	for line in infile:
		fixedline = line
		for replacement in replacements:
			fixedline = replacement[0].sub(replacement[1], fixedline)
		index = 0
		while index < len(fixedline):
			if(ord(fixedline[index]) == 226 and ord(fixedline[index+1]) == 128 and ord(fixedline[index+2]) == 169):
				output.append("\n")
				index += 3
			else:
				output.append(fixedline[index])
				index += 1
	infile.close()
	
	outfile = None
	if options.safe:
		# This is a really ugly way to do this, and it isn't absolutely safe (file could 
		# already exist), but it works for now.
		outfile = open(".out.".join(filename.split(".")), "w")
	else:
		outfile = open(filename, "w")
	
	outfile.write("".join(output))