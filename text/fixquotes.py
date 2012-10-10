#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
files = ['Advanced_Delving.xml', 'Monsters.xml',
'Bard.xml', 'Moves.xml',
'Character_Creation.xml', 'Moves_Discussion.xml',
'Class_Moves_Discussion.xml', 'Paladin.xml',
'Cleric.xml', 'Playing_the_Game.xml',
'Cleric_Spells.xml', 'Ranger.xml',
'Druid.xml', 'The_World.xml',
'Equipment.xml', 'Thief.xml',
'Example.xml', 'Wizard.xml',
'Fighter.xml', 'Wizard_Spells.xml',
'First_Session.xml', 'Fronts.xml', 'GM.xml', 'Introduction.xml',
'appendices/Conversion.xml', 'appendices/NPCs.xml', 'appendices/Teaching.xml', 'appendices/Thanks.xml',
'monster_settings/Caverns.xml','monster_settings/Experiments.xml',
'monster_settings/Hordes.xml','monster_settings/Swamp.xml','monster_settings/Woods.xml',
'monster_settings/Depths.xml','monster_settings/Folk.xml','monster_settings/Planes.xml',
'monster_settings/Undead.xml'
]

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
	outfile.write(''.join(output))
	outfile.close()

	print ''.join(output)
			