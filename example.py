import moodlequiz
import random


def sum_options(x,y):

	options = []
	options.append(f"\item* {x+y}")							# correct option
	options.append(f"\item {x*y}") 							# 'plausible' distractor
	options.append(f"\item {x**y}")							# 'plausible' distractor
	options.append(f"\item {random.choice(range(100))}")	# distractor

	random.shuffle(options)		# not strictly necessary if moodle is set to shuffle options

	return options



if __name__=="__main__":

	Q = moodlequiz.Quiz("example.tex")

	# add 10 variants
	for i in range(10):

		# generate some random variants
		x = random.choice(range(1,10))
		y = random.choice(range(1,10))
		options = sum_options(x,y)

		## define new question data
		data = {}
		data['x'] = x
		data['y'] = y
		data['options'] = '\n'.join(options)

		## add new question to question set
		Q.add_variant(data)

	Q.export("output.tex",compile=True)


