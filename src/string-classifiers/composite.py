
from abstract import AbstractMatcher
from collections import Iterable
import functools

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
		ans = functools.reduce(reduction, results)
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
