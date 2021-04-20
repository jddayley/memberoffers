import xml.etree.ElementTree as ET


def main():
    # use the parse() function to load and parse an XML file
    tree = ET.parse(
        "/Users/ddayley/Dropbox/My Mac (Dons-MacBook-Pro.local)/Desktop/Dev/flaskapp/data/Paper Coupon SAP XML - FOC 5.XML"
    )
    root = tree.getroot()
    for elem in tree.iter():
        print(elem)


# print out the document node and the name of the first child tag

# prettyxml = doc.toprettyxml()
# print(prettyxml)
# # get a list of XML tags from the document and print each one
#    expertise = doc.getElementsByTagName("expertise")
#    print "%d expertise:" % expertise.length
#    for skill in expertise:
#      print skill.getAttribute("name")

# # create a new XML tag and add it into the document
#    newexpertise = doc.createElement("expertise")
#    newexpertise.setAttribute("name", "BigData")
#    doc.firstChild.appendChild(newexpertise)
#    print " "

#    expertise = doc.getElementsByTagName("expertise")
#    print "%d expertise:" % expertise.length
#    for skill in expertise:
#      print skill.getAttribute("name")
if __name__ == "__main__":
    main()
