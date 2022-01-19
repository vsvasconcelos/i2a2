import buscacep
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

arquivo = "/media/vagner/Seagate Expansion Drive/500Gb/DiskExternoVagner/Cursos/CientistaDados/Modulo_4/DW-OSM-RMSP/sample.osm"
#arquivo = r'F:\500Gb\DiskExternoVagner\Cursos\CientistaDados\Modulo_4\DW-OSM-RMSP\sample.osm'

osm_file = open(arquivo, "r")

def audit():
    """     Realiza análise baseada no evento "tag de ínicio"; quando este ocorre o elemento em questão é 
    identificado e se for do tipo "way", o método "iter" é chamado; este método realiza uma iteração de todas as 
    subtags (tags aninhadas) do tipo "tag".
    """
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    #audit_postcode(tag.attrib['v'])
                    valida_cep(tag.attrib['v'])

def is_postcode(elem):
    """     Verifica se o tag é um atributo de (addr:postcode). Retorna um Boolean (True se atributo
    de CEP)           
    """
    return (elem.attrib['k'] == "addr:postcode")

def audit_postcode(postcode):
    """     Utiliza expressão regular para verificar o ínicio do campo "addr:street" identificando assim o Tipo de 
    Via (Rua, Alamenda, etc)
    """
    postcode_re = re.match(r'^\d{5}-\d{3}$', postcode)
    #postcode_re = re.match(r'^\d{5}-?\d{3}$', postcode)  Considerando o "-" opcional
    #print postcode_re
    if postcode_re== None:
        cep_novo = re.split(r'^\d{3}', postcode)
        print postcode, "=>", "com problema" 
        print cep_novo, "=>", "novo" 
    

def valida_cep (postcode):
    postcode_re = re.sub(r'\D',"" ,postcode)
    #res = buscacep.busca_cep_correios(postcode_re)
    aux=True
    while aux:
        try:
            res=buscacep.busca_cep_correios_as_dict(postcode_re)
            print postcode, postcode_re
            pprint.pprint(res)
            break
        except AttributeError:
            print "CEP", postcode, "Nao existe"
            aux=False
    
    
if __name__ == '__main__':
    audit()
    osm_file.close()



