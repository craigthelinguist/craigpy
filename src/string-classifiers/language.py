
from abstract import AbstractClassifier, AbstractMatcher
from collections import Iterable

class LanguageClassifier(AbstractClassifier):

	__categories__ = {}

	def __init__(self, matchers={}):
		if not isinstance(matchers, dict):
			raise TypeError("Must pass dict to the matchers arg of LanguageClassifier, but was passed", type(matchers))
		for matcher in matchers.values():
			if not isinstance(matcher, AbstractMatcher):
				raise TypeError("matchers arg of LanguageClassifier must be mapping of keys to AbstractMacther, but you passed a ", type(matcher))
		self.__categories__ = matchers

	def __classifyone__(self, string):
		results = {}
		for category in self.__categories__:
			matcher = self.__categories__[category]
			result = matcher.match_probability(string)
			results[category] = result
		return results

	def __classifyprobs__(self, strings):
		if isinstance(strings, str):
			return self.__classifyone__(strings)
		elif isinstance(strings, Iterable):
			return [self.__classifyone__(string) for string in strings]

	def __getbest__(self, results):
		mostlikely = None
		for key in results:
			if mostlikely == None or results[key] > mostlikely[1]:
				mostlikely = (key,results[key])
		return mostlikely

	def classify_words(self, strings, probabilities=False):
		if not (isinstance(strings, str) or isinstance(strings, Iterable)):
			raise TypeError("LanguageClassifier can only classify str or Itreable but was asked to classify ", type(strings))
		if not isinstance(probabilities, bool):
			raise TypeError("LanguageClassifier.classify_words arg probabilities must be True or False")
		if probabilities:
			return self.__classifyprobs__(strings)
		else:
			probs = self.__classifyprobs__(strings)
			return self.__getbest__(probs)

	def classify_text(self, text, probabilities=False):
		if not isinstance(text, str):
			raise TypeError("classify_text must be passed a string to classify")
		if not isinstance(probabilities, bool):
			raise TypeError("classify_text's probabilities arg must be True or False")

		# split text
		text = text.split(" ")
		classifications = {}

		# get pcts for each token
		for token in text:
			results = self.__classifyprobs__(token)
			for category in results:
				pct = results[category]
				if category not in classifications:
					classifications[category] = 0.0
				classifications[category] = classifications[category] + pct

		# if you just want biggest, return it now
		if not probabilities:
			return self.__getbest__(results)

		# else norm and return probs
		for category in classifications:
			classifications[category] = classifications[category] / len(text)
		return classifications