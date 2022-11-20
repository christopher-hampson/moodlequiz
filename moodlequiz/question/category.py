from . import Question
from dataclasses import dataclass, field

@dataclass
class Category(Question):
    _type		        : str = field(default="category",kw_only=True)
    category    		: str = field(default="")
    info            	: str = field(default="",metadata={'@format':'moodle_auto_format'})
    idnumber    		: int | None = None