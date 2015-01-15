
import ling as __ling__
from functools import reduce

def __normalise__(map):
	value_count = sum(map.values())
	return { key : 1.0 * map[key] / value_count for key in map }

class Classifier(object):

	ngrams = {}
	classes = {}
	degree = None

	def __init__(self, training, ngram_degree):
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
		for ngram in self.ngrams:
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
		return self.classes[clazz][ngram]

	def prob_class(self, clazz):
		return len(self.classes) / 1.0

	def prob_ngram_class(self, ngram, clazz):
		return self.classes[clazz][ngram]

	def classify(self, string):
		freq = __ling__.ngram_frequency(string, self.degree)
		clazz_probs = { cl : [] for cl in self.classes.keys() }

		for ngram in freq:
			for clazz in self.classes:
				prob_c = self.prob_class(clazz)
				prob_xc = self.prob_ngram_class(ngram, clazz)
				p_i = prob_c * prob_xc
				for i in range(freq[ngram]):
					clazz_probs[clazz].append(p_i)

		for clazz in clazz_probs:
			print(clazz_probs[clazz])

		clazz_probs = { clazz : reduce(lambda x,y : x*y, clazz_probs[clazz])
							for clazz in clazz_probs }

		best_category = None
		best_prob = None
		for clazz in clazz_probs:
			prob = clazz_probs[clazz]
			if best_category == None or prob > best_prob:
				best_prob = prob
				best_category = clazz
		return best_category