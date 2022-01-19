
# coding: utf-8

# In[6]:

#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


osm_file = open("/media/vagner/Seagate Expansion Drive/500Gb/"+
                "DiskExternoVagner/Cursos/CientistaDados/"+
                "Modulo_4/DW-OSM-RMSP/sample.osm", "r")

#file_out = "/media/vagner/Seagate Expansion Drive/500Gb/DiskExternoVagner/Cursos/CientistaDados/Modulo_4/DW-OSM-RMSP/sample2.json"
file_out = "/media/vagner/Seagate Expansion Drive/500Gb/DiskExternoVagner/Cursos/CientistaDados/Modulo_4/DW-OSM-RMSP/sample222.json"

street_type_re = re.compile(r'^\S+\.?',re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

mapping = { "Av": "Avenida",
            "Av.": "Avenida",
            "R": "Rua",
            "R.": "Rua", 
            "rua": "Rua",
            "r.": "Rua",
            "r": "Rua",
            "Pr.": u"Praça",
            "PR.": u"Praça",
            "Complexo viário": u"Complexo Viário",
            "Complexo viario": u"Complexo Viário"
          }

def update_name(name, mapping):
    #print name
    m = street_type_re.search(name)
    other_street_types=[]
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type_re, mapping[street_type], name)
        else:
            other_street_types.append(street_type)
        return name

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        created = {}
        for e in element.attrib.keys():
            if e in CREATED:
                created[e] = element.attrib[e]
            elif  element.attrib[e] == element.get('lat') or element.attrib[e] == element.get('lon'):
                pos = []
                pos.append(float(element.get('lat')))
                pos.append(float(element.get('lon')))
                node['pos'] = pos
            else:
                node[e] = element.get(e)
                node['type'] = element.tag
        node['created'] = created
        node_refs = []
        address = {}
        for subtag in element:
            if subtag.tag == 'tag':
                if re.search(problemchars, subtag.get('k')):
                    pass
                elif re.search(r'\w+:\w+:\w+', subtag.get('k')):
                    pass
                elif subtag.get('k').startswith('addr:'):
                    address_type = subtag.get('k')[5:]
                    if address_type == 'street':
                        address[address_type] = update_name(subtag.get('v'),mapping)
                    else:
                        address[address_type] = subtag.get('v')
                    node['address'] = address
                else:
                    node[subtag.get('k')] = subtag.get('v')
            else:
                if subtag.tag == 'nd':
                    node_refs.append(subtag.get('ref'))
                else:
                    pass
        if node_refs:
            node['node_refs'] = node_refs
        return node
    else:
        return None

    
def process_map(file_in, pretty = False):
    print file_out
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
   
    data = process_map(osm_file, False)
    #pprint.pprint(data)
    
if __name__ == "__main__":
    test()


# In[ ]:



