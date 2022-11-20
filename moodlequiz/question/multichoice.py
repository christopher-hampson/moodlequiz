from .question import GradedQuestion
from dataclasses import dataclass, field
from typing import List
from ..utils import CDATA

@dataclass
class Option:
    fraction 	: float = field(default=0)
    text		: str = field(default="")
    feedback	: str = field(default="")
    format		: str = field(default="html",repr=False)
    feedback_format		: str = field(default="html",repr=False)

    def to_dict(self):
        info = {'@fraction': self.fraction,
            '@format' : self.format,
            'text' : self.text,
            'feedback': {'@format': self.feedback_format, 'text': self.feedback}}
        return info

	
@dataclass
class MultiChoice(GradedQuestion):
    _type 			        : str = "multichoice"
    _answer                 : list = field(default_factory=list)
    single					: bool = field(default=True)
    shuffleanswers			: bool = field(default=True)
    showstandardinstruction	: int = field(default=1) 	# displays whether to select one or multiple options
    answernumbering			: str = field(default="none",metadata={'flat':True})
    correctfeedback			: str = field(default="",metadata={'@format':'html'})
    partiallycorrectfeedback: str = field(default="",metadata={'@format':'html'})
    incorrectfeedback		: str = field(default="",metadata={'@format':'html'})


    def add_option(self,fraction,text:str,feedback:str="") -> None:
        X = Option(fraction,text,feedback)
        self._answer.append(X)

    def as_dict(self):
        info = super().as_dict()
        info['answer'] = [a.to_dict() for a in self._answer]
        return info

    def show_options(self) -> List[Option]:
        return self._answer

    def count_options(self) -> int:
        return len(self._answer)

    def sum_options(self) -> float:
        return sum([float(opt.fraction) for opt in self._answer])