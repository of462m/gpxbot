# Use:
#     https://stackoverflow.com/questions/299588/validating-with-an-xml-schema-in-python

import gpxpy
import gpxpy.gpx
from lxml import etree

# xmlschema_doc = etree.parse('gpx/gpx11.xsd')
# xmlschema = etree.XMLSchema(xmlschema_doc)
#
# try:
#     xml_doc = etree.parse('gpx/2023-07-16T09-27-33Z_001-Архей-ira338.gpx')
#     print(xmlschema.validate(xml_doc))
# except etree.XMLSyntaxError:
#     print('RRROR!')


with open('angara/10.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)


for track in gpx.tracks:
    print(track.name)



