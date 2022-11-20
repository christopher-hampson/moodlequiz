from dataclasses import dataclass, field, fields
from functools import cached_property
import xmltodict
from ..utils import CDATA

@dataclass
class Question:

    @property
    def fields(self):
        '''Returns a list of all fields for the question'''
        return fields(self)

    def export(self,filename):
        '''Exports the prettyxml string of the question to filename'''
        with open(filename,"w") as f:
            f.write(str(self.prettyxml))

    def as_dict(self):
        '''Returns a dictionary containing all the question details'''
        info = {'@type': self._type}
        for key in self.fields:
            ## get attribute value and metadata
            val = getattr(self,str(key.name))
            metadata = key.metadata

            ## skip internal fields
            if key.name.startswith("_"): 
                continue

            

            ## format html objects as CDATA tag    
            elif metadata.get('@format')=="html":
                val = CDATA(val)

            ## no special formatting
            if metadata.get("flat"):
                info[key.name] = val
            elif key.type == str:
                base = dict(key.metadata)
                base['text'] = val
                info[key.name] = base
            else:
                info[key.name] = val
        return info

    @property
    def xml(self):
        '''Returns a string of the Question XML without indentation'''
        return xmltodict.unparse(self.as_dict(),pretty=False)

    @property
    def prettyxml(self):
        '''Returns a pretty string of the Question XML with indentation'''
        return xmltodict.unparse(self.as_dict(),pretty=True)

@dataclass
class GradedQuestion(Question):
    name			: str = field(default="Default Name")
    questiontext	: str = field(default="",metadata={'@format':'html'})
    defaultgrade	: int = field(default=10)
    penalty			: float = field(default=0)
    hidden			: int = field(default=0)
    idnumber		: str = field(default=" ",metadata={'flat':True})
    generalfeedback	: str = field(default="",metadata={'@format':'html'})