#!/usr/bin/env python

#
#
# Script to add shortcodes to cnxmlplus files

import sys
import lxml.etree as etree

import dencoder

def zero_pad_shortcode(shortcode, character):
    '''Pad on the left "shortcode" with character. Asumed shortcodes will be 4 chars long'''
    return '{s:{c}>{n}}'.format(s=shortcode, n=4,c=character)


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
        if element.tag == 'section':
            element.insert(element.index(element.find('title'))+1, newShortcode)
        else:
            element.insert(0, newShortcode)
    else:
        shortcodetag.text = shortcode

    return element

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 5:
        print '''Usage: %s listofxmlfiles.txt SectionPrefix SectionStart ExStart
        
Adds shortcodes to sections and problem sets in cnxmlplus files. Writes to standard output

listofxmlfiles: txt file containing filenames for xml files containing chapters of a book, one per line
SectionPrefix: String that gets appended to shortcode
SectionStart: starting shortcode for sections
ExStart: starting shortcode for problems''' %args[0]
        sys.exit(1)

    # Encoder
    Dencoder = dencoder.Dencoder(alphabet=dencoder.Dencoder.SIYAVULA_ALPHABET)
    
    SectionPrefix = sys.argv[2]
    SectionStart = Dencoder.decode(sys.argv[3])
    ExStart = Dencoder.decode(sys.argv[4])

    for f in open(sys.argv[1], 'r').readlines():
        print f.strip(), 'Start', zero_pad_shortcode(Dencoder.encode(ExStart), '2'), SectionPrefix+zero_pad_shortcode(Dencoder.encode(SectionStart), '2')
        xmlfile = etree.parse(f.strip())
        root = xmlfile.getroot()

        # remove all shortcode elements
        for element in root.iter():
            if element.tag == 'shortcode':
                element.getparent().remove(element)


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
                newshortcode = zero_pad_shortcode(Dencoder.encode(ExStart), '2')
                element = addShortcodeTag(element, newshortcode)
                ExStart += 1

            
            # shortcodes for /document/content//exercises//problem-set/entry
            if element.tag in ['entry', 'multi-part']:
                # check if the parent is exercises or problem-set
                if element.getparent().tag in ['exercises', 'problem-set']:
                    newshortcode = zero_pad_shortcode(Dencoder.encode(ExStart), '2')
                    element = addShortcodeTag(element, newshortcode)
                    ExStart += 1

        #print etree.tostring(root, encoding='utf-8')
        newXMLFile = open(f.strip(), 'w').write(etree.tostring(root, encoding='utf-8', xml_declaration=True))
        print f.strip(), 'End',  zero_pad_shortcode(Dencoder.encode(ExStart-1), '2'), SectionPrefix+zero_pad_shortcode(Dencoder.encode(SectionStart-1), '2')
