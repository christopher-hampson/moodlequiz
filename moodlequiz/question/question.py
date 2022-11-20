from typing import Any
import xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field, fields
# from ..datatypes import *
from functools import cached_property
import xmltodict
from ..utils import CDATA

@dataclass
class Question:
    ## Data validation and defaults
    # name			: str = field(default="Default Name",metadata={'@format':'plaintext'})
    # questiontext	: str = field(default="",metadata={'@format':'html'})
    # defaultgrade	: int = field(default=10)
    # penalty			: float = field(default=0)
    # hidden			: int = field(default=0)
    # idnumber		: str = field(default=" ")
    # generalfeedback	: str = field(default="",metadata={'@format':'html'})

    @property
    def fields(self):
        '''Returns a list of all fields for the question'''
        return fields(self)

    # def set_plaintext(self,key:str,value:str):
    #     X = ET.Element(key)
    #     txt = ET.SubElement(X,"text")
    #     txt.text = str(value)
    #     return X

    # def set_single(self,key:str,value:str):
    #     X = ET.Element(str(key))
    #     X.text = str(value)
    #     return X

    # def set_cdata(self,key:str,value:str):
    #     X = ET.Element(key)
    #     X.append(CDATA(str(value)))
    #     return X

    # def set_html(self,key:str,value:str):
    #     X = ET.Element(key)
    #     X.set('format','html')
    #     txt = ET.SubElement(X,"text")
    #     txt.append(CDATA(str(value)))
    #     return X

    def export(self,filename):
        '''Exports the prettyxml string of the question to filename'''
        with open(filename,"w") as f:
            f.write(str(self.prettyxml))

    def as_dict(self):
        info = {'@type': self.type}
        for key in self.fields:
            val = getattr(self,str(key.name))

            metadata = key.metadata

            if metadata.get('@format')=="html":
                val = CDATA(val)

            if key.type == str:
                base = dict(key.metadata)
                base['text'] = val
                info[key.name] = base
            else:
                info[key.name] = val
        return info

    @cached_property
    def xml_old(self):
        '''Returns a string of the Question XML'''
        xml = ET.Element("question")
        xml.set('type',self._question_type)
        
        for X in fields(self):
            print(X.name,X.metadata)
            if X.name.startswith("_") and not X.metadata.get('name',None): 
                continue
            name = X.metadata.get('name',X.name)
            property = X.metadata.get('property',name)
            # name = X.name 
            value = getattr(self,property)
            metadata = X.metadata.get('xml',None)

            if metadata=="html":
                xml.append(self.set_html(name,value))

            elif metadata=="plaintext":
                xml.append(self.set_plaintext(name,value))

            elif metadata=="cdata":
                xml.append(self.set_cdata(name,value))

            elif metadata=="list":
                for item in value:
                    xml.append(item.xml)


            else:
                xml.append(self.set_single(name,value))


        return xml

    @property
    def prettyxml(self):
        '''Returns a pretty string of the Question XML with tabulation'''
        return xmltodict.unparse(self.to_dict(),pretty=True)
        return minidom.parseString(self.xml).toprettyxml(indent="    ")

@dataclass
class GradedQuestion(Question):
    name			: str = field(default="Default Name")
    questiontext	: str = field(default="",metadata={'@format':'html'})
    defaultgrade	: int = field(default=10)
    penalty			: float = field(default=0)
    hidden			: int = field(default=0)
    idnumber		: str = field(default=" ")
    generalfeedback	: str = field(default="",metadata={'@format':'html'})