
# coding: utf-8

# In[16]:

#!/usr/bin/env python

#audit.py
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

arquivo = "/media/vagner/Seagate Expansion Drive/500Gb/DiskExternoVagner/Cursos/CientistaDados/Modulo_4/DW-OSM-RMSP/sample.osm"

osm_file = open(arquivo, "r")

street_type_re = re.compile(r'^\S+\.?',re.IGNORECASE)
street_types = defaultdict(set)



expected = ["Alameda", "Avenida", "Estrada", "Largo", u"Praça", "Rodovia", "Rua", "Travessa", "Via",
            u"Calçadão", "Rodoanel", "Passeio", u"Complexo Viário", "Marginal"]

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

def audit_street_type(street_types, street_name):
    """     Utiliza expressão regular para verificar o ínicio do campo "addr:street" identificando assim o Tipo de 
    Via (Rua, Alamenda, etc)
    """
    #print street_name
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        #print street_type 
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def is_street_name(elem):
    """     Verifica se o tag é um atributo de endereço de via (addr:street). Retorna um Boolean (True se atributo
    de endereço de via)           
    """
    return (elem.attrib['k'] == "addr:street")

def audit():
    """     Realiza análise baseada no evento "tag de ínicio"; quando este ocorre o elemento em questão é 
    identificado e se for do tipo "way", o método "iter" é chamado; este método realiza uma iteração de todas as 
    subtags (tags aninhadas) do tipo "tag".
    """
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    #pprint.pprint(dict(street_types))
    return street_types

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

def test():
    st_types = audit()
    print (len(st_types.keys()))
    #pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
        if name != better_name:
            print name, "=>", better_name
            name= better_name
              
if __name__ == '__main__':
    test()
    osm_file.close()


# In[ ]:



