
import re
import xml.sax.saxutils
escape = xml.sax.saxutils.escape
def escape_hacked(data, entities={}):
    '''Hack xml.sax.saxutils to prevent escaping CDATA tags'''
    m = re.match(r"<!\[CDATA\[([\s\S]*)\]\]>",data)
    if m:
        inner = escape(m.group(1),entities)
        return f"<![CDATA[{inner}]]>"

    return escape(data, entities)
xml.sax.saxutils.escape = escape_hacked

from .quiz import *
from .question import *