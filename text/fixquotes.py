#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
files = ['monster_settings/Swamp.xml']

for filename in files:
	output = []
	file = open(filename, 'r')
	
	for line in file:
		outputline = line[0]
		
		prevchar = line[0]
		inTag = prevchar == "<"
		for character in line[1:]:
			if inTag:
				outputline += character
			elif character == "'":
				outputline += "’"
			elif character == '"' and (prevchar == " " or prevchar == '>'):
				outputline += '“'
			elif character == '"':
				outputline += '”'
			else:
				outputline += character
				
			if character == ">":
				inTag = False
			if character == "<":
				inTag = True
			prevchar = character
		
		output.append(outputline)
	
	file.close()
	
	outfile = open(filename, 'w')
	outfile.write(print ''.join(output))
	outfile.close()

	print ''.join(output)
			