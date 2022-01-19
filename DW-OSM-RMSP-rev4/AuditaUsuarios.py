#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re


osm_file = open("/media/vagner/Seagate Expansion Drive/500Gb/"+
                "DiskExternoVagner/Cursos/CientistaDados/"+
                "Modulo_4/DW-OSM-RMSP/sample.osm", "r")


def get_user(element):

    if element.get('uid'):
        uid = element.attrib["uid"]
        return uid
    else:

        return None


def process_map():
    users = set()
    for _, element in ET.iterparse(osm_file):
        if get_user(element):
            users.add(element.attrib["uid"])
    return users

def test():

    users = process_map()
    print len(users)
    print(users)
    
if __name__ == "__main__":
    test()
    osm_file.close()

