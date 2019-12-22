"""
File: bayes.py
Original Author: code is written from 'Think Bayes'
"""
# Conditional Probability #
# A conditional probability is a probability based on some background information.
### p(A | B) := "The probability of A happening, given that B is true."

# Conjoint Probability #
# Knowing the probability of one event does not affect the second, because 
# the events are independent.
### p(A and B) := "The probability that A and B are both true." 


### Short desccription of Baye's Theorem:
### p(A | B) = [p(A) p( B| A)] / p(B) for any events A and B.

# The diachronic interpretation of Baye's Thm #
# This interpretation helps us update the probability of some hypothesis, H, in light of some
# body of new data, D.

# p(H | D) = [p(H) p(D | H)] / p(D)

### p(H) := istheprobabilityofthehypothesisbeforeweseethedata,called the prior probability, or just 'prior'.
### p(H|D) := iswhatwewanttocompute,theprobabilityofthehypothesis after we see the data, called the 'posterior'.
### p(D|H) := is the probability of the data under the hypothesis, called the 'likelihood'.
### p(D) := is the probability of the data under any hypothesis, called the 'normalizing constant'.

# Sometimes the 'prior' can be computed based on background information

# Here we will use the probability mass function on the cookie problem.

from thinkbayes import Pmf
pmf = Pmf()

pmf.Set('Bowl 1', 0.5)
pmf.Set('Bowl 2', 0.5)
pmf.Mult('Bowl 1', 0.75)
pmf.Mult('Bowl 2', 0.5)

pmf.Normalize()
print(pmf.Prob('Bowl 1'))

print('\n')
print('The Cookie Problem: ')
# The Cookie problem #
# In the following class a Cookie object is a Pmf that maps from hypotheses to their probabilities.
# the __init__ method gives each hypothesis the same prior probanility.
class Cookie(Pmf):
	def __init__(self, hypos):
		Pmf.__init__(self)
		for hypo in hypos:
			self.Set(hypo, 1)
		self.Normalize()
	def Update(self, data):
		for hypo in self.Values():
			like = self.Likelihood(data, hypo)
			self.Mult(hypo, like)
		self.Normalize()
	mixes = {
	'Bowl 1':dict(vanilla=0.75, chocolate=0.25),
	'Bowl 2':dict(vanilla=0.5, chocolate=0.5)
	}

	def Likelihood(self, data, hypo):
		mix = self.mixes[hypo]
		like = mix[data]
		return like
hypos = ['Bowl 1', 'Bowl 2']
pmf = Cookie(hypos)
	# Cookie provides an Update method that takes data as a parameter and updates the probabilities:
	# Update loops through each hypothesis in the suite and muiltiplies its probability by the likelihood
	# of the data under the hypothesis.

pmf.Update('vanilla')

for hypo, prob in pmf.Items():
		print(hypo, prob)

print('\n')

dataset = ['vanilla', 'chocolate', 'vanilla']
for data in dataset:
	pmf.Update(data)

# The lines below will show different probabilities.

for data, prob in pmf.Items():
		print(data, prob)

print('\n')
print('The Monty Hall Problem:')
print('\n')

# The Monty Hall Problem #

# We will solve this problem using a class.

class Monty(Pmf):
	def __init__(self, hypos):
		Pmf.__init__(self)
		for hypo in hypos:
			self.Set(hypo, 1)
		self.Normalize()

	def Update(self, data):
		for hypo in self.Values():
			like = self.Likelihood(data, hypo)
			self.Mult(hypo, like)
		self.Normalize()
# The main difference between the Cookie problem and Monty Hall is in the 'Likelihood' method...
	def Likelihood(self, data, hypo):
		if hypo == data:
			return 0
		elif hypo == 'A':
			return 0.5
		else:
			return 1


hypos = 'ABC'
pmf = Monty(hypos)

data = 'B'
pmf.Update(data)

for hypo, prob in pmf.Items():
	print(hypo, prob)


from thinkbayes import Suite

class Monty(Suite):

	def Likelihood(sefl, data, hypo):
		if hypo == data:
			return 0

		elif hypo == 'A':
			return 0.5

		else:
			return 1

def main():
	suite = Monty('ABC')
	suite.Update('B')
	suite.Print()

if __name__ == '__main__':
	main()

print('\n')
print('M&M Problem: ')
print('\n')

## The M&M Problem ##
class M_and_M(Suite):
	mix94 = dict(brown=30, 
				 yellow=20,
				 red=20,
				 green=10,
				 orange=10,
				 tan=10)
	mix96 = dict(blue=24,
				 green=20,
				 orange=16,
				 yellow=14,
				 red=13,
				 brown=13)

	hypoA = dict(bag1=mix94, bag2=mix96)
	hypoB = dict(bag1=mix96, bag2=mix94)
	hypotheses = dict(A=hypoA, B=hypoB)

	def Likelihood(self, data, hypo):
		bag, color = data
		mix = self.hypotheses[hypo][bag]
		like = mix[color]
		return like

def main():
	suite = M_and_M('AB')

	suite.Update(('bag1', 'yellow'))
	suite.Update(('bag2', 'green'))

	suite.Print()

if __name__ == '__main__':
	main()

print('\n')
print('Playing with D&D Dice: ')
print('\n')

# The Suite class only provides an implentation of 'Update', even though it includes the
# interface for 'Likelihood'.

## Estimation ##
# The Dice problem:

# We will use integers to represent our data here.
# The list of intergers represents the set of die, and how
# many sides ae on each of the die.

class Dice(Suite):
	def Likelihood(self, data, hypo):
		if hypo < data: 			# Since we can't have a roll that gives data larger than the number of sides,
			return 0 				# we return probability 0.
		else:
			return 1.0/hypo 		# Otherwise we give the chance of rolling that data point.

def main():
	suite = Dice([4, 6, 8, 12, 20])

	suite.Update(6)
	print('After one 6')
	suite.Print()

	for roll in [6, 8, 7, 7, 4]:
		suite.Update(roll)

	print('After more rolls')
	suite.Print()

if __name__ == '__main__':
	main()

# The Locomotive Problem #
# A railroad numbers its locomotives in order from 1...N. One day you see a locomotive numbered 60.
# Estimate how many locomotives the railroad has.
# Based on that observation, we know that the railroad has 60 or more locomotives. But how many more?
# Applying Baysian reasoning:
# 1) What did we know about N before we saw the data?
# 2) For any given N, what is the likelihood of seeing the data(a locomotive with #60)?
# The answer to 1) is the 'prior'. The answer to 2) is the likelihood.

# Assume that N is equally likely to be any value between 1 and 1000.

print('\n')
print('Locomotive Problem: ')
print('Calculates mean of posterior distribution for finding a car with #60:')
print('\n')

import thinkplot
hypos = range(1, 1001)

class Train(Dice):
	"""Represents hypotheses about how many trains the company has.

	The likelihood function for the train problem is the same as
	for the Dice problme. So we just call the Dice class into the
	train class.
	"""

def main():
	hypos = range(1, 1001)
	suite = Train(hypos)

	suite.Update(60)
	print(suite.Mean())

	thinkplot.PrePlot(1)
	thinkplot.Pmf(suite)
	thinkplot.Save(root='train1',
				   xlabel='Number of Trains',
				   ylabel='Probability',
				   formats=['pdf', 'eps'])



if __name__ == '__main__':
	main()