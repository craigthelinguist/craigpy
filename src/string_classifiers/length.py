
import numbers as __numbers__
from collections import Iterable
from abstract import * 

class LengthClassifier(AbstractClassifier):

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
			raise NotImplementedError("LengthClassifier must be set up with LengthClassifier.stdev or LengthClassifier.range")

	def match(self, words, returntype="list"):
		if isinstance(words, str):
			return self.__matchone__(words)
		elif isinstance(words, Iterable):
			return [word for word in words if __matchone__(word)]
		else:
			raise TypeError("LengthClassifier can only classify Strings and Iterables.") 

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