
class AbstractClassifier():

	__inverted__ = False

	def match(self, words):
		raise NotImplementedError()

	def match_probability(self, words):
		raise NotImplementedError()

	def invert(self):
		self.__inverted__ = not self.__inverted__

	def is_inverted(self):
		return self.__inverted__
