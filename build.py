#!/usr/bin/env python
# Dungeon World -> pseudo-HTML
# Adam Blinkinsop <github.com/blinks>

import glob
import re
import xml.etree.ElementTree as etree

# Pattern to read chapters in a way that enables sorting.
CHAPTER = re.compile(r'(\d+|[a-z])(\d+|[a-z])?-.*\.xml')


def main():
  """Adds all chapters to a single HTML file and writes it out."""
  tree = etree.ElementTree(etree.fromstring(u"""
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>Dungeon World</title>
      <style type="text/css">
        html, body { width: 800px; margin: 1em auto; }
        span { text-shadow: 0 0 0.2em #aaf; }
      </style>
    </head>
    <body>
    </body>
  </html>
  """))
  body = tree.find('body')
  for filename in smartsorted(glob.iglob('*-*.xml')):
    chapter = etree.parse(filename)

    # Change the root into a top-level element.
    root = chapter.getroot()
    root.tag = 'section'
    root.set('id', filename)

    # Deal with Story/Body elements in a more html-ish way.
    story = root.find('Story')
    if story is None: story = root.find('Body')
    if story is not None:
      story.tag = 'div'
      story.set('class', 'story')

    body.append(root)
  tree.write('book.html', encoding='utf-8', method='html')


def smartsorted(iterator):
  """Ensures chapters are read in the right order."""
  def keyfn(value):
    m = CHAPTER.match(value)
    assert m is not None
    key = [m.group(1), m.group(2) or '0']
    return tuple([k.isdigit() and int(k) or ord(k) for k in key])
  return sorted(iterator, key=keyfn)


if __name__ == '__main__':
  main()
