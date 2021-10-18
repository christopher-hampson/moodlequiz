import moodlequiz
import random


def sum_options(x,y):
	## simple example

	options = []
	options.append(f"\item* {(x+y)}")							# correct option
	options.append(f"\item {(x*y)}") 							# 'plausible' distractor
	options.append(f"\item {(x-y)}")							# 'plausible' distractor
	options.append(f"\item {(random.choice(range(100)))}")		# distractor

	random.shuffle(options)		# not strictly necessary if moodle is set to shuffle options

	return options



if __name__=="__main__":

	## load the LaTeX template 'example.tex'
	Q = moodlequiz.Quiz("example.tex")

	# add 10 variants
	for i in range(10):

		# generate some random variants
		x = random.choice(range(1,10))
		y = random.choice(range(1,10))
		options = sum_options(x,y)

		## define new question data to be replaced
		## this will substitute commands \x, \y, and \options in the TeX
		data = {}
		data['x'] = x
		data['y'] = y
		data['options'] = '\n'.join(options)

		## add new question to question set
		Q.add_variant(data)

		## alternatively 'add_variant' accepts a list of keyword arguments
		#Q.add_variant(x=x,y=y,options='\n'.join(options))


	## generate new LaTeX file output populated with question variants
	## 'compile' will also compile the output with pdfLaTeX, which will also generate an XML file.
	Q.export("output.tex",compile=True)


