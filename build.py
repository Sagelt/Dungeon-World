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
        html, body {
          font: 16px sans-serif;
          margin: 1em auto;
          width: 800px;
        }
        p { margin: 0.5em 0; padding: 0; }
        span { text-shadow: 0 0 0.5em #aaf; }
        p, span { text-indent: 1em; }

        h1 {
          border-bottom: 1px solid gray;
          font-size: 24px;
          margin-top: 2em;
          padding-bottom: 0.5em;
          text-align: center;
        }
        h2 {
          border-bottom: 1px solid #aaa;
          font-size: 20px;
          margin-top: 1.5em;
        }
        h3 { font-size: 18px; }

        .Example {
          margin: 0 1em;
          padding: 0.5em;
          border: 1px solid #bbb;
          background-color: #eee;
        }
        .MoveName, .BasicMoveName { text-shadow: 0 0 0.5em #afa; }
        .NoIndent { text-indent: 0; }
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
    for story in root.findall('Story') + root.findall('Body'):
      story.tag = 'div'
      story.set('class', 'story')

    class_attrs = ['{http://ns.adobe.com/AdobeInDesign/4.0/}pstyle']
    for e in root.iter('*'):
      for attr in class_attrs:
        if e.get(attr) is not None:
          e.set('class', e.get(attr))

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
