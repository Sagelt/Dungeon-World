#!/usr/bin/env python
# Dungeon World -> pseudo-HTML
# Adam Blinkinsop <github.com/blinks>
#
# TODO: Figure out how to nicely deal with Root / Story nodes.

import glob
import re
import xml.dom.minidom as minidom

CHAPTER = re.compile(r'(\d+|[a-z])(\d+|[a-z])?-.*\.xml')

def main():
  """Adds all chapters to a single HTML file and writes it out."""
  book = minidom.parseString(u'<html><head></head><body></body></html>')
  body = book.documentElement.childNodes[1]

  for filename in smartsorted(glob.iglob('*-*.xml')):
    doc = minidom.parse(filename)

    chapter = book.createElement('section')
    for child in doc.childNodes:
      chapter.appendChild(child)
    body.appendChild(chapter)

  writexml(book, open('book.html', 'w'))

def smartsorted(iterator):
  """Ensures chapters are read in the right order."""
  def keyfn(value):
    m = CHAPTER.match(value)
    assert m is not None
    key = [m.group(1), m.group(2) or '0']
    return tuple([k.isdigit() and int(k) or ord(k) for k in key])
  return sorted(iterator, key=keyfn)

def writexml(doc, writer):
  writer.write(doc.toxml('utf-8'))

if __name__ == '__main__':
  main()
