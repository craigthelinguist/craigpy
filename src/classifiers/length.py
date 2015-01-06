
import numbers as __numbers__
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
		if self.__minlength__ == None and self.__maxlength__ == None:
			raise NotImplementedError("LengthClassifier must be set up with LengthClassifier.stdev or LengthClassifier.range")
		if isinstance(words, str):
			return self.__matchone__(words)
		elif isinstance(words, Iterable):
			return [word for word in words if __matchone__(word)]
		else:
			raise TypeError("LengthClassifier can only classify Strings and Iterables.") 

	def stdev(self, mean, stdev, acceptable_stdevs):
		if not isinstance(stdev, __numbers__.Number) or not isinstance(acceptable_stdevs, __numbers__.Number):
			raise ArithmeticError("Must pass numbers to arguments minlength and maxlength. You passed: ("+str(type(minlength))+","+str(type(maxlength))+")")
		self.__minlength__ = mean - stdev * acceptable_stdevs
		self.__maxlength__ = mean + stdev * acceptable_stdevs

	def range(self, minlength, maxlength):
		if not isinstance(minlength, __numbers__.Number) or (not isinstance(maxlength, __numbers__.Number) and maxlength!="infinity"):
			raise ArithmeticError("Must pass numbers to arguments minlength and maxlength. You passed: ("+str(type(minlength))+","+str(type(maxlength))+")")
		self.__minlength__ = minlength
		if maxlength != "infinity":
			self.__maxlength__ = maxlength

