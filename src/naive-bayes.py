
import ling as __ling__
from functools import reduce

def __normalise__(map):
	value_count = sum(map.values())
	return { key : 1.0 * map[key] / value_count for key in map }

class Classifier(object):

	ngrams = {}
	classes = {}
	degree = None

	def __init__(training, ngram_degree):
		'''
		training
			[(Iterable, str), (Iterable, str)]
		ngram_degree

		'''
		self.degree = ngram_degree

		# get frequency count
		for tuple in training:
			examples = tuple[0]
			name = tuple[1]
			self.classes[name] = {}
			for example in examples:
				freq = ling.ngram_frequency(example, ngram_degree)
				for ngram in freq:
					if ngram not in self.classes[name]:
						self.classes[name][ngram] = 1
					else:
						self.classes[name][ngram] += 1
					if ngram not in self.ngrams:
						self.ngrams[ngram] = 1
					else:
						self.ngrams[ngram] += 1

		# turn everything into probabilities
		__normalise__(ngrams)
		for clazz in self.classes:
			__normalise__(self.classes[clazz])

	def prob_ngram(ngram):
		return self.ngrams[ngram]

	def prob_class(clazz):
		return len(self.classes) / 1.0

	def prob_ngram_class(ngram, clazz):
		return self.classes[clazz][ngram]

	def classify(string):
		freq = ling.ngram_frequency(string, self.degree)
		clazz_probs = { cl : [] for cl in self.classes.keys() }

		for ngram in freq:
			for clazz in self.classes:
				prob_c = prob_class(clazz)
				prob_xc = prob(ngram, clazz)
				p_i = prob_c * prob_xc
				clazz_probs[clazz].append(p_i)

		clazz_probs = { key : reduce(lambda x,y : x*y, clazz_probs[key]) }
		best_category = None
		best_prob = None
		for clazz in clazz_probs:
			prob = clazz_probs[clazz]
			if best_category == None or prob > best_prob:
				best_prob = prob
				best_category = clazz
		return best_category