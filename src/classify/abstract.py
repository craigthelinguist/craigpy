
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
