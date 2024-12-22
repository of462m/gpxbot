import os
from lxml import etree
# import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx

gpx10_xmlschema_doc = etree.parse('gpx/gpx10.xsd')
gpx10_xmlschema = etree.XMLSchema(gpx10_xmlschema_doc)
gpx11_xmlschema_doc = etree.parse('gpx/gpx11.xsd')
gpx11_xmlschema = etree.XMLSchema(gpx11_xmlschema_doc)

pic_dir = 'angara'
# pic_dir = 'angara'

for fname in os.listdir(pic_dir):
    fname = f'{pic_dir}/{fname}'
    print(fname, end='\t')
    try:
        xml_doc = etree.parse(fname)
        root = xml_doc.getroot()
        if root.attrib['version'] == '1.0':
            isval = gpx10_xmlschema.validate(xml_doc)
        elif root.attrib['version'] == '1.1':
            isval = gpx11_xmlschema.validate(xml_doc)

        if not isval:
            print(f"{isval}\tgpx: {root.attrib['version']}\tcreator: {root.attrib['creator']}")
        else:
            gpx_file = open(fname, 'r', encoding=xml_doc.docinfo.encoding)
            gpx = gpxpy.parse(gpx_file)
            # for waypoint in gpx.waypoints:
            #     print(f'{isval}\tcreator: {gpx.creator}\t\t\t{waypoint.name}')
            for track in gpx.tracks:
                try:
                    if track.name.lower().find('монды') != -1:
                        print(f'FIND {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
                    else:
                        print(f'NOTFIND: {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
                except AttributeError:
                    print(f'NOTFIND(exc): {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')

    except (etree.XMLSyntaxError, KeyError, UnicodeDecodeError):
        print(Exception.args)


    # gpx_file = open(f'{pic_dir}/{fname}', 'r')
    # gpx = gpxpy.parse(gpx_file)
    # for track in gpx.tracks:
    #     print(f'{fname}\t{track.name}')