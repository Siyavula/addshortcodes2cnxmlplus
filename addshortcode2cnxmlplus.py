#!/usr/bin/env python

#
#
# Script to add shortcodes to cnxmlplus files

import sys
import lxml.etree as etree

import dencoder

def addShortcodeTag(element, shortcode):
    '''checks if element has shortcode tag as a child, replaces the contents
    with the given shortcode or creates a new shortcode element and returns the
    given element'''
    # Check if there is a shortcode tag, and if not add one
    shortcodetag = element.find('shortcode')
    if shortcodetag is None:
        newShortcode = etree.Element('shortcode')
        newShortcode.text = shortcode
        newShortcode.tail = '\n'
        element.insert(0, newShortcode)
    else:
        shortcodetag.text = shortcode

    return element

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 5:
        print '''Usage: %s cnxmlplusfile.cnxmlplus SectionPrefix SectionStart ExStart
        
Adds shortcodes to sections and problem sets in cnxmlplus file. Writes to standard output

SectionPrefix: String that gets appended to shortcode
SectionStart: starting shortcode for sections
ExStart: starting shortcode for problems''' %args[0]
        sys.exit(1)

    # Encoder
    Dencoder = dencoder.Dencoder(alphabet=dencoder.Dencoder.SIYAVULA_ALPHABET)
    
    SectionPrefix = sys.argv[2]
    SectionStart = Dencoder.decode(sys.argv[3])
    ExStart = Dencoder.decode(sys.argv[4])

    xmlfile = etree.parse(sys.argv[1])
    root = xmlfile.getroot()

    for element in root.iter():
        path = r'/'.join(reversed([a.tag for a in element.iterancestors()])) +\
        r'/' + str(element.tag)
        
        # Add section shortcodes
        if element.tag == 'section':
            if (path == r'document/content/section/section') or (path ==
                    r'document/content/section/section/section'):
                # These are sections and subsections
                newshortcode = SectionPrefix + Dencoder.encode(SectionStart)
                element = addShortcodeTag(element, newshortcode) 
                SectionStart += 1
        
        # Rich media shortcodes
        if element.tag in ['presentation', 'simulation', 'video']:
            # maybe create better shortcode for simulations, presentations and
            # videos
            newshortcode = 'V' + Dencoder.encode(ExStart)
            element = addShortcodeTag(element, newshortcode)
            ExStart += 1

        
        # shortcodes for /document/content//exercises//problem-set/entry
        if element.tag == 'entry':
            # check if the parents contain exercises and problem-set
            if ('exercises' in path) and ('problem-set' in path):
                newshortcode = Dencoder.encode(ExStart)
                element = addShortcodeTag(element, newshortcode)
                ExStart += 1

        # shortcodes for /document/content//exercises//multi-part
        if element.tag == 'multi-part':
            # check if the parents contain exercises 
            if ('exercises' in path):
                newshortcode = Dencoder.encode(ExStart)
                element = addShortcodeTag(element, newshortcode)
                ExStart += 1

    print etree.tostring(root, encoding='utf-8')
