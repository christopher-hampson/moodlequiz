from . import GradedQuestion
from dataclasses import dataclass, field

@dataclass
class Essay(GradedQuestion):
    type		: str = "essay"
    responseformat		: str = field(default="editor",repr=False)
    responsefieldlines	: int = field(default=15,repr=False)
    attachments			: int = field(default=0)
    attachmentsrequired	: int = field(default=0)
    filetypeslist 		: str = field(default="")
    graderinfo			: str = field(default="", metadata={'@format':'html'})
    responsetemplate	: str = field(default="", metadata={'@format':'html'})
