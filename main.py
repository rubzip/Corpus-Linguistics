from lxml import etree


fname = ""
parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parser(fname, parser)

for elem in tree.xpath(""):
    pass