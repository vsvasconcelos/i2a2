
# coding: utf-8

# In[1]:

#!/usr/bin/env python

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("/media/vagner/Seagate Expansion Drive/500Gb/"+
                "DiskExternoVagner/Cursos/CientistaDados/"+
                "Modulo_4/DW-OSM-RMSP/sample.osm", "r")


street_type_re = re.compile(r'^\S+\.?',re.IGNORECASE)
    # Módulo de expressões regulares para comparar uma sequência de caracteres que não sejam espaço em branco,
    # talvez seguido por um ponto - isto é, abreviações ex.: Aven. (Avenida) - no inicio da string (^).
    # Ex. "Rodov. Anhaguera" ou "RoD. ANHAGUERA"
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    """     Realiza analise do nome das ruas (street_name) buscando
    pelos tipos existentes na base (street_types).  
    Argumentos:
            Recebe os tipos de ruas válidos e o nome da rua lido           
    Retornos:
            Não possui 
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    cont=0;
    contV=0;
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 
        cont+=1
        contV=contV+v
    print cont
    print contV

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    """     Examina o arquivo XML, um tag por vez, utilizando um analisador Sax, de forma a criar um registro
    de todos os street_types encontrados no conjunto de dados.
    Argumentos:
            Não possui           
    Retornos: 
            Não possui 
    """
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()


# In[ ]:



