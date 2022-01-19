
# coding: utf-8

# In[ ]:

#!/usr/bin/env python

"""
Contagem dos tags
"""
import xml.etree.cElementTree as ET
import pprint

osm_file = open("/media/vagner/Seagate Expansion Drive/500Gb/"+
                "DiskExternoVagner/Cursos/CientistaDados/"+
                "Modulo_4/DW-OSM-RMSP/sample.osm", "r")

tags = count_tags(osm_file)
pprint.pprint(tags)

def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename):
            if elem.tag in tags:
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1
        return tags

