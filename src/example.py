
import classifiers

def maori_matcher():
	with open("../corpora/maori-corpus.txt", "r") as f:
		corpus = [line.rstrip() for line in f]
		return classifiers.CorpusMatcher(0.5, trainingSet=corpus)

def english_matcher():
	with open("../corpora/english-corpus.txt", "r") as f:
		corpus = [line.rstrip() for line in f]
		return classifiers.CorpusMatcher(0.5, trainingSet=corpus)

def language_classifier():
	en = english_matcher()
	mi = maori_matcher()
	return classifiers.LanguageClassifier({"English" : en, "Maori" : mi})

words = ["johnny", "korero", "whakapapa", "dragon", "help", "kitten", "kitchen", "egypt", "aotearoa", "auckland", "akarana"]
lc = language_classifier()


print("=============================================")
print(lc.classify_words("john", probabilities=False))
print("=============================================")
print(lc.classify_words("john", probabilities=True))
print("=============================================")
print(lc.classify_words(words, probabilities=False))
print("=============================================")
print(lc.classify_words(words, probabilities=True))

