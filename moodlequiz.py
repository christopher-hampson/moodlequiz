import os, copy
import TexSoup

class Quiz:

	def __init__(self,*args):
		if len(args)>0:
			self.set_template(args[0])

	def set_template(self,template):
		self.__template = template
		self.__variants = []
		self.parse_template()

	def parse_template(self):
		with open(self.__template,"r") as f:
			src = f.read()
			self.soup = TexSoup.TexSoup(src)
			self.__questions = self.soup.find("quiz").contents[-1]
			self.template = TexSoup.TexSoup(src)
			for x in self.template.find("quiz").children:
				self.template.find("quiz").remove(x)


	def add_variant(self,params):
		X = TexSoup.TexSoup(str(self.__questions.expr))
		for key in params:
			X.find(key).replace_with(params[key])
		self.__variants.append(X)


	def export(self,filename='output.tex',compile=False):
		self.__texfile = os.path.abspath(filename).split(".")

		self.template.find('quiz').insert(0,*self.__variants)
		with open(filename,"w") as f:
			f.write(str(self.template)) 

		if compile:
			os.system("mkdir build")
			os.system(f"pdflatex --output-dir=build -synctex=0 -interaction=nonstopmode {filename}")





Q = Quiz("scc/scc_quiz_template.tex")
# Q.set_template("scc/scc_quiz_template.tex")
question_set = [{'first':1,'last':2,'second':'33','third':'7656','diagram':''}]
Q.add_variant(question_set[0])
Q.add_variant(question_set[0])
Q.add_variant(question_set[0])
Q.add_variant(question_set[0])
Q.export("aug-2021_test.tex",compile=True)
