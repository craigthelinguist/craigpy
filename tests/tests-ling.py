import inspect
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, "../src")))

from ling import *

def assertion(assertion, correct_msg, failure_msg):
	if assertion:
		print(correct_msg)
		return True
	else:
		print(failure_msg)
		return False

def test_seq_score_1():
	s1 = "john"
	s2 = "ohm"
	ans = seq_align(s1, s2)
	correct_ans = -1
	return assertion(ans==correct_ans,
		"Passed seq_score_1",
		"Failed seq_score_1: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_2():
	s1 = "john"
	ans = seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_2",
		"Failed seq_score_2: got " + str(ans) + " but should have been 4")

def test_seq_score_3():
	s1 = "john"
	ans = seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_3",
		"Failed seq_score_3: got " + str(ans) + " but should have been 4")

def test_seq_score_4():
	s1 = "john"
	s2=  "John"
	ans = seq_align(s1, s2, case_sensitive=True)
	return assertion(ans==2,
		"Passed seq_score_4",
		"Failed seq_score_4: got " + str(ans) + " but should have been 2")

def test_seq_score_5():
	s1 = "john"
	s2 = "ohm"
	ans = seq_align(s1, s2, match=4, mismatch=-5, skip=-10)
	correct_ans = -7
	return assertion(ans==correct_ans,
		"Passed seq_score_5",
		"Failed seq_score_5: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_6():
	s1 = "john"
	s2 = "JoHn"
	ans = seq_align(s1, s2, match=2, mismatch=-3, skip=-5, case_sensitive=True)
	correct_ans = - 3 + 2 - 3 + 2
	return assertion(ans==correct_ans,
		"Passed seq_score_6",
		"Failed seq_score_6: got "+ str(ans) +" but should have been " + str(correct_ans))

def test_seq_align_1():
	s1 = "john"
	s2 = "ohm"
	align = alignment(s1, s2)
	correct_ans = ("john","_ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_1",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

def test_seq_align_2():
	s1 = "john"
	s2 = "ohm"
	align = alignment(s1, s2, pad_character="&")
	correct_ans = ("john", "&ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_2",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

def test_jaccard_1():
	s1 = "ab"
	s2 = "ab"
	index = jaccard(s1,s2,1)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_1",
		"Failed jaccard_1: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_2():
	s1 = "ab"
	s2 = "ab"
	index = jaccard(s1,s2,2)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_2",
		"Failed jaccard_2: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_3():
	s1 = "abcd"
	s2 = "efgh"
	index = jaccard(s1,s2,1)
	correct_ans = 0.0
	return assertion(index == correct_ans,
		"Passed jaccard_3",
		"Failed jaccard_3: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_4():
	s1 = "abcd"
	s2 = "abba"
	index = jaccard(s1,s2,1)
	correct_ans = 0.5
	return assertion(index == correct_ans,
		"Passed jaccard_3",
		"Failed jaccard_3: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_5():
	s1 = "abcd"
	s2 = "abba"
	index = jaccard(s1,s2,2)
	correct_ans = 0.2
	return assertion(index == correct_ans,
		"Passed jaccard_4",
		"Failed jaccard_4: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_6():
	s1 = ""
	index = jaccard(s1,s1,1)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_5",
		"Failed jaccard_5: got " + str(index) + " but should have been " + str(correct_ans))

def test_ngram_1():
	s1 = "hello"
	ngram = ngram_frequency(s1, 1)
	claim = ngram["h"] == 1 and ngram["e"] == 1 and ngram["l"] == 2 and ngram["o"] == 1
	return assertion(claim,
		"Passed ngram_1",
		"Failed ngram_1: frequency count of 1-grams was wrong")

def test_ngram_2():
	s1 = "hellenes"
	ngram = ngram_frequency(s1, 2)
	claim = ngram["he"] == 1 and ngram["el"] == 1 and ngram["ll"] == 1 and ngram["le"] == 1 and ngram["en"] == 1 and ngram["ne"] == 1 and ngram["es"] == 1
	return assertion(claim,
		"Passed ngram_2",
		"Failed ngram_2: frequency count of 2-grams was wrong")

def test_ngram_3():
	s1 = "billy"
	ngram = ngram_set(s1, 1)
	claim = "b" in ngram and "i" in ngram and "l" in ngram and "y" in ngram and len(ngram) == 4
	return assertion(claim,
		"Passed ngram_3",
		"Failed ngram_3: returned set was wrong")

def test_ngram_4():
	s1 = "clarissa"
	ngram = ngram_set(s1, 2)
	claim = "cl" in ngram and "la" in ngram and "ar" in ngram and "ri" in ngram and "is" in ngram and "ss" in ngram and "sa" in ngram and len(ngram) == 7
	return assertion(claim,
		"Passed ngram_4",
		"Failed ngram_4: frequency count of 2-grams was wrong")

def test_ngram_5():
	s1 = "johnny"
	ngram = ngram_frequency(s1, 1)
	claim = ngram["j"] == 1 and ngram["o"] == 1 and ngram["h"] == 1 and ngram["n"] == 2 and ngram["y"] == 1 and len(ngram) == 5
	return assertion(claim,
		"Passed ngram_5",
		"Failed ngram_5: frequency count was" + str(ngram))

def test_ngram_6():
	s1 = "johnny"
	ngram = ngram_frequency(s1, 2)
	claim = ngram["jo"]==1 and ngram["oh"]==1 and ngram["hn"]==1 and ngram["nn"]==1 and ngram["ny"]==1 and len(ngram)==5
	return assertion(claim,
		"Passed ngram_6",
		"Failed ngram_6: frequency count was " + str(ngram))

def test_ngram_7():
	s1 = "john"
	ngram = ngram_frequency(s1, 1, normed=True)
	claim = ngram["j"]==0.25 and ngram["o"]==0.25 and ngram["h"]==0.25 and ngram["n"]==0.25 and len(ngram)==4
	return assertion(claim,
		"Passed ngram_7",
		"Failed ngram_7: prob count was " + str(ngram))

def test_ngram_8():
	s1 = "john"
	ngram = ngram_frequency(s1, 2, normed=True)
	third = 1.0 / 3
	claim = ngram["jo"]==third and ngram["oh"]==third and ngram["hn"]==third and len(ngram)==3 and sum(ngram.values())==1.0
	return assertion(claim,
		"Passed ngram_8",
		"Failed ngram_8: prob count was " +  str(ngram))

def main():
	print("=================")
	print("Running tests....")
	print()
	tests = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith("test"))]
	sortkey = lambda x : str(x)
	tests.sort(key=sortkey)
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