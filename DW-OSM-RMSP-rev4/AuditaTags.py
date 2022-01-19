
# coding: utf-8

# In[ ]:

#tags.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

osm_file = open("/media/vagner/Vag1T_Disk/"+
                "discoExterno/Cursos/CientistaDados/"+
                "ND_AnalistaDados/P3-LimpandoDadosDoOpenStreetMap/Projeto/sample.osm", "r")

def key_type(element, keys):
    if element.tag == "tag":
        if lower.match (element.attrib['k']):
            keys['lower']+=1
        elif lower_colon.match(element.attrib['k']):
            keys['lower_colon']+=1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars']+=1
        else:
            keys['other']+=1
    return keys



def process_map():
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(osm_file):
        keys = key_type(element, keys)

    return keys



def test():
    
    keys = process_map()
    pprint.pprint(keys)
   


if __name__ == "__main__":
    test()
    osm_file.close()

