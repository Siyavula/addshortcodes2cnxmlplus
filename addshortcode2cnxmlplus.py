#!/usr/bin/env python

#
#
# Script to add shortcodes to cnxmlplus files

import sys
import lxml.etree as etree

import dencoder

#     /document/content//exercises//problem-set/entry
#     /document/content//presentation
#     /document/content//simulation
#     /document/content//video

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 5:
        print '''Usage: %s cnxmlplusfile.cnxmlplus SectionPrefix SectionStartValue ExStartValue
        
Adds shortcodes to sections and problem sets in cnxmlplus file. Writes to standard output

SectionPrefix: String that gets appended to shortcode
SectionStartValue: integer number where first section shortcode starts
ExStartValue: integer number where first solution shortcode starts''' %args[0]
        sys.exit(1)

    SectionPrefix = sys.argv[2]
    SectionStartValue = int(sys.argv[3])
    ExStartValue = int(sys.argv[4])

    xmlfile = etree.parse(sys.argv[1])
    root = xmlfile.getroot()


    # Encoder
    Dencoder = dencoder.Dencoder(alphabet=dencoder.Dencoder.SIYAVULA_ALPHABET)
    
    for element in root.iter():
        path = r'/'.join(reversed([a.tag for a in element.iterancestors()]))  #TODO bug, add tag name
        
        # Add section shortcodes
        if element.tag == 'section':
            if (path == r'document/content/section') or (path == r'document/content/section/section'):
                # These are sections and subsections

                # Check if there is a shortcode tag, and if not add one
                shortcodetag = element.find('shortcode')
                if shortcodetag is None:
                    newShortcode = etree.Element('shortcode')
                    newShortcode.text = SectionPrefix + Dencoder.encode(SectionStartValue)
                    newShortcode.tail = '\n'
                    element.insert(0, newShortcode)
                else:
                    shortcodetag.text = SectionPrefix + Dencoder.encode(SectionStartValue)

                SectionStartValue += 1




    print etree.tostring(root, encoding='utf-8')
