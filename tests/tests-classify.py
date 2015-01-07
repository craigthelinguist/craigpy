import inspect
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, "../src")))

from classifiers import *

def assertion(assertion, correct_msg, failure_msg):
	if assertion:
		print(correct_msg)
		return True
	else:
		print(failure_msg)
		return False

def maori_matcher():
	with open("../corpora/maori-corpus.txt", "r") as f:
		corpus = [line.rstrip() for line in f]
		return CorpusMatcher(0.5, trainingSet=corpus)

def english_matcher():
	with open("../corpora/english-corpus.txt", "r") as f:
		corpus = [line.rstrip() for line in f]
		return CorpusMatcher(0.5, trainingSet=corpus)

def language_classifier():
	return LanguageClassifier({"English" : english_matcher(), "Maori" : maori_matcher()})

def test_classification_1():
	text1 = "Hey, how are you? My name is Aaron. It's good to meet you. I'm currently typing this out and I'm thinking of things to say but I'm not so great at that. Here's a really long piece of text that I hope makes for a good test."
	classifier = language_classifier()
	ans = classifier.classify_text(text1)
	pct = round(ans[1] * 100, 2)
	fail_msg = ans[0] + "("+str(pct)+"%)"
	return assertion(ans[0] == "English",
		"test_classification_1 passed.",
		"test_classification_1 failed: is English but was classified as " + fail_msg)

def test_classification_2():
	text1 = "kia ora e hoa. ko hemi toku ingoa. kei te wananga o wikitoria, e ako ana. ko matai te tohu, ahakoa, ehara tena i te pai ki ahau."
	classifier = language_classifier()
	ans = classifier.classify_text(text1)
	pct = round(ans[1] * 100, 2)
	fail_msg = ans[0] + "("+str(pct)+"%)"
	return assertion(ans[0] == "Maori",
		"test_classification_2 passed.",
		"test_classification_2 failed: is Maori but was classified as " + fail_msg)
 
def main():

	tests = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith("test"))]
	sortkey = lambda x : str(x)
	tests.sort(key=sortkey)
	print("=================")
	print(len(tests), "tests.")
	print("Running tests....")
	print()
	count = 0
	for test in tests:
		if test():
			count = count + 1
	pct = 1.0 * count / len(tests) * 100
	print()
	print("Finished.")
	print("Passed: " + str(count) + "/" + str(len(tests)) + " ("+str(pct)+"%)")
	print("================")
	
if __name__ == "__main__":
	main()