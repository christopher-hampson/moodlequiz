import xmltodict
from dataclasses import dataclass
from .question import Question



@dataclass
class Quiz:
    question = []

    def __init__(self,filename=None):
        pass

    def add_question(self,question:Question) -> None:
        '''Add a new question of type Question to the quiz'''
        if not isinstance(question,Question):
            raise Exception("Expected object of type 'Question'.")
        self.question.append(question)

    def to_dict(self) -> dict:
        '''Returns a dictionary containing all the quiz details'''
        return {'quiz': {'question': [q.as_dict() for q in self.question]}}

    @property
    def xml(self) -> str:
        '''Returns a string of the Quiz XML without indendation'''
        return xmltodict.unparse(self.to_dict(),pretty=False)

    @property
    def prettyxml(self) -> str:
        '''Returns a pretty string of the Quiz XML with indentation'''
        return xmltodict.unparse(self.to_dict(),pretty=True)


    def export(self,filename:str="output.xml") -> None:
        '''Writes xml of quiz to file'''
        with open(filename,"w") as f:
            f.write(self.prettyxml)
        print(f"Written to file '{filename}'")


