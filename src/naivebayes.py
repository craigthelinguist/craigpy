
import ling as __ling__
from functools import reduce

def __normalise__(map):
	value_count = sum(map.values())
	return { key : 1.0 * map[key] / value_count for key in map }

class Classifier(object):

	ngrams = {}
	classes = {}
	degree = None

	def __init__(self, training, ngram_degree, alphabet):
		'''
		training
			[(Iterable, str), (Iterable, str)]
		ngram_degree

		'''

		self.ngrams = {}
		self.classes = {}
		self.degree = ngram_degree

		# get frequency count
		for tuple in training:
			examples = tuple[0]
			name = tuple[1]
			self.classes[name] = {}
			for example in examples:
				freq = __ling__.ngram_frequency(example, ngram_degree)
				for ngram in freq:
					if ngram not in self.classes[name]:
						self.classes[name][ngram] = 1
					else:
						self.classes[name][ngram] += 1
					if ngram not in self.ngrams:
						self.ngrams[ngram] = 1
					else:
						self.ngrams[ngram] += 1

		# laplace smooting
		for ngram in alphabet:

			# for the ngrams
			if ngram not in self.ngrams:
				self.ngrams[ngram] = 1
			else:
				self.ngrams[ngram] += 1

			# for each class
			for clazz in self.classes:
				if ngram not in self.classes[clazz]:
					self.classes[clazz][ngram] = 1
				else:
					self.classes[clazz][ngram] += 1

		# turn everything into probabilities
		self.ngrams = __normalise__(self.ngrams)
		for clazz in self.classes:
			self.classes[clazz] = __normalise__(self.classes[clazz])

	def prob_ngram(self, ngram):
		return self.ngrams[ngram]

	def prob_class(self, clazz):
		return len(self.classes) / 1.0

	def prob_ngram_class(self, ngram, clazz):
		return self.classes[clazz][ngram]

	def classify(self, string):

		# these strings cannot be classified!
		if (len(string) < self.degree):
			return None

		# get frequency count for the ngrams in the string
		freq = __ling__.ngram_frequency(string, self.degree)
		clazz_probs = { cl : [] for cl in self.classes.keys() }

		# create a vector of probabilites for each ngram for each class
		for ngram in freq:
			for clazz in self.classes:
				prob_c = self.prob_class(clazz)
				prob_xc = self.prob_ngram_class(ngram, clazz)
				p_i = prob_c * prob_xc
				for i in range(freq[ngram]):
					clazz_probs[clazz].append(p_i)

		# debugging purposes
		# outputs the vector of probabilities for each class
		#for clazz in clazz_probs:
		#	print(clazz_probs[clazz])


		# reduce the probability vectors into a probability for that one class
		# map each class's probability vector to its aggregated probability
		for clazz in clazz_probs:
			pvector = clazz_probs[clazz]
			if len(pvector) == 0:
				pvector = [0]
			p = reduce(lambda x,y : x*y, pvector)
			clazz_probs[clazz] = p

		# return the class with the highest probability
		best_category = None
		best_prob = None
		for clazz in clazz_probs:
			prob = clazz_probs[clazz]
			if best_category == None or prob > best_prob:
				best_prob = prob
				best_category = clazz
		return best_category

	def test(self, testset):
		hits = 0
		misses = 0
		for pair in testset:
			string = pair[0]
			category = pair[1]
			if self.classify(string) == category:
				hits += 1
			else:
				misses += 1
		total = hits + misses
		prob = 1.0 * hits / total * 100
		prob = round(prob, 2)
		print("accuracy: " + str(prob) + "% ("+str(hits)+"/"+str(total)+")") 