

from abstract import AbstractMatcher
from collections import Iterable

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
