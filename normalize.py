import os
from lxml import etree
# import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx

if __name__ == '__main__':

    pic_dir = 'angara'
    # for fname in os.listdir(pic_dir):
    #     nn = int(os.path.splitext(fname)[0])
    #     new_fname = f"{nn:03}.gpx"
    #     print(f"name={nn}.gpx -> {new_fname}")
    #     os.rename(f"{pic_dir}/{fname}", f'{pic_dir}/{new_fname}')
    #
    # exit(0)

    gpx10_xmlschema_doc = etree.parse('gpx/gpx10.xsd')
    gpx10_xmlschema = etree.XMLSchema(gpx10_xmlschema_doc)
    gpx11_xmlschema_doc = etree.parse('gpx/gpx11.xsd')
    gpx11_xmlschema = etree.XMLSchema(gpx11_xmlschema_doc)


    with open('enisey/dvalidation.txt', 'w', encoding='utf-8') as fout:

        for fname in os.listdir(pic_dir):
            fname = f'{pic_dir}/{fname}'

            try:
                xml_doc = etree.parse(fname)
                root = xml_doc.getroot()
                if root.attrib['version'] == '1.0':
                    isval = gpx10_xmlschema.validate(xml_doc)
                elif root.attrib['version'] == '1.1':
                    isval = gpx11_xmlschema.validate(xml_doc)

                str2file = f"{fname}\t{xml_doc.docinfo.encoding.lower()}\t{isval}\t{root.attrib['version']}\t{root.attrib['creator']}"
                print(f"Writing: {str2file}")
                fout.write(f"{str2file}\n")

                # if not isval:
                #     print(f"{fname}:{isval}\tgpx: {root.attrib['version']}\tcreator: {root.attrib['creator']}")
                # else:
                #     pass
                    # gpx_file = open(fname, 'r', encoding=xml_doc.docinfo.encoding)
                    # gpx = gpxpy.parse(gpx_file)
                    # # for waypoint in gpx.waypoints:
                    # #     print(f'{isval}\tcreator: {gpx.creator}\t\t\t{waypoint.name}')
                    # for track in gpx.tracks:
                    #     try:
                    #         if track.name.lower().find('монды') != -1:
                    #             print(f'FIND {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
                    #         else:
                    #             print(f'NOTFIND: {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')
                    #     except AttributeError:
                    #         print(f'NOTFIND(exc): {isval}\tcreator: {gpx.creator}\t\t\t{track.name}')

            except (etree.XMLSyntaxError, KeyError, UnicodeDecodeError) as err:
                print("Упал-отжался!")
                print(err)


            # gpx_file = open(f'{pic_dir}/{fname}', 'r')
            # gpx = gpxpy.parse(gpx_file)
            # for track in gpx.tracks:
            #     print(f'{fname}\t{track.name}')