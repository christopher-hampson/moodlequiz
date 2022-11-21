import json


class Feedback:
    '''A class for improving ease of writing feedback'''
    _feedback = []
    score = 0
    total_marks = 1

    def __init__(self,total_marks=1) -> None:
        self.total_marks = total_marks

    def resultcolumns(self):
        return str([["Feedback",'feebdack']])

    def __add__(self,other):
        F = Feedback(total_marks = self.total_marks+other.total_marks)
        F.score = self.score + other.score
        F.feedback = self.feedback + other.feedback
        return F

    def append(self,feedback,score=0) -> None:
        self._feedback.append(feedback)
        self.score += score

    @property
    def feedback(self) -> str:
        return "\n".join(self._feedback)

    @property
    def fraction(self) -> float:
        return self.score/self.total_marks

    def __str__(self) -> str:
        return json.dumps({'feedback':self.feedback,'fraction':self.fraction})

