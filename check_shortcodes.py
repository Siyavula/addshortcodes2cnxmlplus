import lxml.etree as etree


myfilelist = open('myfiles.txt', 'r').readlines()


shortcodes = []

for f in myfilelist:
    root = etree.parse(f.strip()).getroot()
    for s in root.iter('shortcode'):
        if s.text in shortcodes:
            print "{0} is duplicate in file {1}".format(s.text, f)
        shortcodes.append(s.text)


print len(shortcodes), len(set(shortcodes))
