
from collections import Iterable
from functools import reduce
import numbers as __numbers__


class AbstractClassifier():

	__categories__ = {}

	def classify_words(self, words, probabilities=False):
		raise NotImplementedError()

	def classify_text(self, text, probabilities=False):
		raise NotImplementedError()

class AbstractMatcher():

	__inverted__ = False

	def match_word(self, words):
		raise NotImplementedError()

	def match_text(self, words):
		raise NotImplementedError()

	def invert(self):
		self.__inverted__ = not self.__inverted__

	def is_inverted(self):
		return self.__inverted__




class CorpusMatcher(AbstractMatcher):

	def __init__(self, threshold, trainingSet=[]):
		if not isinstance(threshold, float) or threshold < 0 or threshold > 1:
			raise TypeError("Threshold must be a float between 0 and 1.")
		if not isinstance(trainingSet, Iterable):
			raise TypeError("CorpusMatcher trainingSet must be Iterable.")
		self.__trainingSet__ = trainingSet
		self.__threshold__ = threshold
		self.train(trainingSet)

	def __getvalue__(self, c1, c2):
		if c1 not in self.__frequencies__:
			return 0
		elif c2 not in self.__frequencies__[c1]:
			return 0
		else:
			return self.__frequencies__[c1][c2]

	def __matchval__(self, string):
		string = string.lower()
		if len(string) == 0:
			return 0
		if len(string) == 1:
			return 1 if string[0] in self.__frequencies__ else 0
		sum_value = 0
		for i in range(len(string)-1):
			c1 = string[i]
			c2 = string[i+1]
			val = self.__getvalue__(c1,c2)
			sum_value = sum_value + val
		return 1.0 * sum_value / (len(string)-1)

	def train(self, trainingSet):
		frequencies = {}

		# helper method
		def insert(c1, c2):
			if c1 not in frequencies:
				frequencies[c1] = {}
			if c2 not in frequencies[c1]:
				frequencies[c1][c2] = 1
			else:
				frequencies[c1][c2] = frequencies[c1][c2] + 1

		# get word count
		for word in trainingSet:
			for i in range(len(word)-1):
				c1 = word[i]
				c2 = word[i+1]
				insert(c1,c2)

		# normalise
		for char in frequencies:
			fmap = frequencies[char]
			total = sum(fmap.values())
			for successor in fmap:
				value = fmap[successor]
				normed = value * 1.0 / total
				fmap[successor] = normed

		self.__frequencies__ = frequencies

	def match_probability(self, strings):
		if isinstance(strings, str):
			return self.__matchval__(strings)
		elif isinstance(strings, Iterable):
			return [self.__matchval__(s) for s in strings]
		else:
			raise TypeError("Can only match str or Iterable.")
    
	def match_word(self, strings):
		prob = self.match_probability(strings)
		return (prob >= self.__threshold__) != self.__inverted__

	def match_text(self, strings, split=None):
		prob = self.match_text_probability(strings, split)
		return (prob >= self.__threshold__) != self.__inverted__

	def match_text_probability(self, strings, split=None):
		if split != None:
			strings = strings.split(split)
		matched = 0
		for s in strings:
			if self.match_word(s):
				matched = matched + 1
		return 1.0 * matched / len(strings)






class CompositeMatcher(AbstractMatcher):

	def __init__(self, matchers, type="or"):
		if not isinstance(matchers, Iterable):
			raise TypeError("Must pass an Iterable to CompositeMatcher constructor.")
		if type not in ["or","and"]:
			raise TypeError('Must pass "or" or "and" to CompositeMatcher constructor')
		self.__matchers__ = []
		for cl in matchers:
			self.__matchers__.append(cl)
		self.__type__ = type

	def __matchone__(self, string):
		results = [cl.match(string) for cl in self.__matchers__]
		if self.__type__ == "or":
			reduction = lambda x,y : x or y
		elif self.__type__ == "and":
			reduction = lambda x,y : x and y
		ans = reduce(reduction, results)
		return ans != self.__inverted__

	def match_probability(self, strings):
		if isinstance(strings, str):
			return match

	def match(self, strings):
		if isinstance(strings, str):
			return self.__matchone__(strings)
		elif isinstance(strings, Iterable):
			return [self.__matchone__(word) for word in strings]
		else:
			raise TypeError("CompositeMatcher can only match str or Iterable")








class LengthMatcher(AbstractMatcher):

	__minlength__ = None
	__maxlength__ = None

	def __matchone__(self, word):
		if self.__minlength__ and self.__maxlength__:
			return (len(word) >= self.__minlength__ and len(word) <= self.__maxlength__) != self.__inverted__
		elif self.__minlength__:
			return (len(word) >= self.__minlength__) != self.__inverted__
		elif self.__maxlength__:
			return (len(word) <= self.__maxlength__) != self.__inverted__
		else:
			raise NotImplementedError("LengthMatcher must be set up with LengthMatcher.stdev or LengthMatcher.range")

	def match(self, words, returntype="list"):
		if isinstance(words, str):
			return self.__matchone__(words)
		elif isinstance(words, Iterable):
			return [word for word in words if __matchone__(word)]
		else:
			raise TypeError("LengthMatcher can only classify Strings and Iterables.") 

	def stdev(self, mean, stdev, acceptable_stdevs):
		if not isinstance(stdev, __numbers__.Number) or not isinstance(acceptable_stdevs, __numbers__.Number):
			raise TypeError("Must pass numbers to arguments minlength and maxlength. You passed: ("+str(type(minlength))+","+str(type(maxlength))+")")
		self.__minlength__ = mean - stdev * acceptable_stdevs
		self.__maxlength__ = mean + stdev * acceptable_stdevs

	def stdev_from_words(self, words, acceptable_stdevs):
		if not isinstance(words, Iterable):
			raise TypeError("stdev_from_words requires an Iterable. You passed: "+str(type(words)))

		word_lengths = [len(word) for word in words]
		mean = lambda x : 1.0 * sum(x) / len(x)
		length_mean = mean(word_lengths)
		residuals = [(wordlength - length_mean)**2 for wordlength in word_lengths]
		length_stdev = mean(residuals)**0.5
		self.stdev(length_mean, length_stdev, acceptable_stdevs)

	def range(self, minlength, maxlength):
		if not isinstance(minlength, __numbers__.Number) or (not isinstance(maxlength, __numbers__.Number) and maxlength!="infinity"):
			raise TypeError("Must pass numbers to arguments minlength and maxlength. You passed: ("+str(type(minlength))+","+str(type(maxlength))+")")
		self.__minlength__ = minlength
		if maxlength != "infinity":
			self.__maxlength__ = maxlength

	def get_range(self):
		return (__minlength__,__maxlength__)










class LanguageClassifier(AbstractClassifier):

	__categories__ = {}

	def __init__(self, matchers={}):
		if not isinstance(matchers, dict):
			raise TypeError("Must pass dict to the matchers arg of LanguageClassifier, but was passed", type(matchers))
		for matcher in matchers.values():
			if not isinstance(matcher, AbstractMatcher):
				raise TypeError("matchers arg of LanguageClassifier must be mapping of keys to AbstractMacther, but you passed a ", type(matcher))
		self.__categories__ = matchers

	def classify_text(self, text, all_classifications=False):
		'''
		Given a string of text, return the category that best fits this text.

		Parameters
		----------
		text : str
			the text to classify. Assumed to be space-delimited
		all_classifications : bool
			if True, return the most likely classification and how likely they fit e.g.: ("Maori", 0.4)
			if False, return all classifications and how likely they fit e.g.: {"Maori" : 0.4, "English" : 0.2}
		
		Return
		------
		all_classifications == True
			return: { "Maori" : 0.6, "English" : 0.3 }
		all_classifications == False
			return: ("Maori", 0.6)
		'''

		# split by spaces, get scores for each word
		text = text.split(" ")
		word_categorisations = self.classify_words(text, all_classifications=True)

		# aggregate scores across all words
		# e.g.: { "korero" : {"Maori" : 0.6, "English" : 0.2}, "whakapapa" : {"Maori" : 0.7, "English" : 0.4}}
		#           will return {"Maori" : 1.3 : "English" : 0.6} 
		categories = {}
		for word in word_categorisations:
			classification_scores = word_categorisations[word]
			for category in classification_scores:
				fit = classification_scores[category]
				if category not in categories:
					categories[category] = 0.0
				categories[category] = categories[category] + fit

		# norm the aggregated scores
		num_words = len(word_categorisations)
		for category in categories:
			categories[category] = categories[category] / num_words

		# return
		if all_classifications:
			return categories
		else:
			return self.__getmostlikely__(categories)

	def classify_words(self, words, all_classifications=False):
		'''
		Given one or more words, return the category which best fits.
		Return: depends on parameters.

		Parameters
		----------
		words : str or Iterable
			the words you want to classify.
		all_classifications : bool
			whether you want to return the fit for all categories (True) or just the fit for the most likely category

		Return
		------
		type(words) == str and all_classifications == True
			return: {"English" : 0.3, "Maori" : 0.6}
		type(words) == str and all_classifications == False
			return ("Maori", 0.6)
		type(words) == Iterable and all_classifications == True
			return: {"korero" : {"English" : 0.2, "Maori" : 0.5}, "whakapapa" : {"English" : 0.4 , "Maori" : 0.7}}
		type(words) == Iterable and all_classifications == False
			return: {"korero" : ("Maori", 0.5), "whakapapa" : ("Maori", 0.7)} 
		'''

		if not isinstance(all_classifications, bool):
			raise TypeError("LanguageClassifier.classify_words arg all_classifications must be True or False")

		if isinstance(words, str):
			strings = [words]
		elif isinstance(words, Iterable):
			strings = words
		else:
			raise TypeError("LanguageClassifier can only classify str or Itreable but was asked to classify ", type(strings))

		wordmapping = {}
		for word in strings:
			probs = self.__getfmap__(word)
			if not all_classifications:
				mostlikely = self.__getmostlikely__(probs)
				wordmapping[word] = mostlikely
			else:
				wordmapping[word] = probs

		if isinstance(words, str):
			return wordmapping[words]
		else:
			return wordmapping

	def __getfmap__(self, string):
		'''
		Take a single string, return mapping of categories to score.
		E.g.: __getfmap__(word) ---> {"Maori" : 0.6, English : "0.2"}}}
		Take a single string, return {"Maori" : 0.7, "English" : 0.4"}
		'''
		results = {}
		for category in self.__categories__:
			matcher = self.__categories__[category]
			result = matcher.match_probability(string)
			results[category] = result
		return results

	def __getmostlikely__(self, probability_map):
		'''
		Take a mapping of categories and return the most likely category.
		E.g.: __getmostlikely__({"Maori" : 0.7, "English" : 0.4}) --> ("Maori", 0.7)
		'''
		mostlikely = None
		for category in probability_map:
			pct = probability_map[category]
			if mostlikely == None or pct > mostlikely[1]:
				mostlikely = (category, pct)
		return mostlikely

