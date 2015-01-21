import inspect
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, "../src")))

from ling import *
from decimal import Decimal
from functools import reduce

def assertion(assertion, correct_msg, failure_msg):
	if assertion:
		print(correct_msg)
		return True
	else:
		print(failure_msg)
		return False

def accurate(test, expected, threshold=0.00001):
	return abs(test - expected) <= threshold

def test_seq_score_01():
	s1 = "john"
	s2 = "ohm"
	ans = seq_align(s1, s2)
	correct_ans = -1
	return assertion(ans==correct_ans,
		"Passed seq_score_1",
		"Failed seq_score_1: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_02():
	s1 = "john"
	ans = seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_2",
		"Failed seq_score_2: got " + str(ans) + " but should have been 4")

def test_seq_score_03():
	s1 = "john"
	ans = seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_3",
		"Failed seq_score_3: got " + str(ans) + " but should have been 4")

def test_seq_score_04():
	s1 = "john"
	s2=  "John"
	ans = seq_align(s1, s2, case_sensitive=True)
	return assertion(ans==2,
		"Passed seq_score_4",
		"Failed seq_score_4: got " + str(ans) + " but should have been 2")

def test_seq_score_05():
	s1 = "john"
	s2 = "ohm"
	ans = seq_align(s1, s2, match=4, mismatch=-5, skip=-10)
	correct_ans = -7
	return assertion(ans==correct_ans,
		"Passed seq_score_5",
		"Failed seq_score_5: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_06():
	s1 = "john"
	s2 = "JoHn"
	ans = seq_align(s1, s2, match=2, mismatch=-3, skip=-5, case_sensitive=True)
	correct_ans = - 3 + 2 - 3 + 2
	return assertion(ans==correct_ans,
		"Passed seq_score_6",
		"Failed seq_score_6: got "+ str(ans) +" but should have been " + str(correct_ans))

def test_seq_align_01():
	s1 = "john"
	s2 = "ohm"
	align = alignment(s1, s2)
	correct_ans = ("john","_ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_1",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

def test_seq_align_02():
	s1 = "john"
	s2 = "ohm"
	align = alignment(s1, s2, pad_character="&")
	correct_ans = ("john", "&ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_2",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

def test_jaccard_01():
	s1 = "ab"
	s2 = "ab"
	index = jaccard(s1,s2,1)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_1",
		"Failed jaccard_1: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_02():
	s1 = "ab"
	s2 = "ab"
	index = jaccard(s1,s2,2)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_2",
		"Failed jaccard_2: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_03():
	s1 = "abcd"
	s2 = "efgh"
	index = jaccard(s1,s2,1)
	correct_ans = 0.0
	return assertion(index == correct_ans,
		"Passed jaccard_3",
		"Failed jaccard_3: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_04():
	s1 = "abcd"
	s2 = "abba"
	index = jaccard(s1,s2,1)
	correct_ans = 0.5
	return assertion(index == correct_ans,
		"Passed jaccard_3",
		"Failed jaccard_3: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_05():
	s1 = "abcd"
	s2 = "abba"
	index = jaccard(s1,s2,2)
	correct_ans = 0.2
	return assertion(index == correct_ans,
		"Passed jaccard_4",
		"Failed jaccard_4: got " + str(index) + " but should have been " + str(correct_ans))

def test_jaccard_06():
	s1 = ""
	index = jaccard(s1,s1,1)
	correct_ans = 1.0
	return assertion(index == correct_ans,
		"Passed jaccard_5",
		"Failed jaccard_5: got " + str(index) + " but should have been " + str(correct_ans))

def test_ngram_01():
	s1 = "hello"
	ngram = ngram_frequency(s1, 1)
	claim = ngram["h"] == 1 and ngram["e"] == 1 and ngram["l"] == 2 and ngram["o"] == 1
	return assertion(claim,
		"Passed ngram_1",
		"Failed ngram_1: frequency count of 1-grams was wrong")

def test_ngram_02():
	s1 = "hellenes"
	ngram = ngram_frequency(s1, 2)
	claim = ngram["he"] == 1 and ngram["el"] == 1 and ngram["ll"] == 1 and ngram["le"] == 1 and ngram["en"] == 1 and ngram["ne"] == 1 and ngram["es"] == 1
	return assertion(claim,
		"Passed ngram_2",
		"Failed ngram_2: frequency count of 2-grams was wrong")

def test_ngram_03():
	s1 = "billy"
	ngram = ngram_set(s1, 1)
	claim = "b" in ngram and "i" in ngram and "l" in ngram and "y" in ngram and len(ngram) == 4
	return assertion(claim,
		"Passed ngram_3",
		"Failed ngram_3: returned set was wrong")

def test_ngram_04():
	s1 = "clarissa"
	ngram = ngram_set(s1, 2)
	claim = "cl" in ngram and "la" in ngram and "ar" in ngram and "ri" in ngram and "is" in ngram and "ss" in ngram and "sa" in ngram and len(ngram) == 7
	return assertion(claim,
		"Passed ngram_4",
		"Failed ngram_4: frequency count of 2-grams was wrong")

def test_ngram_05():
	s1 = "johnny"
	ngram = ngram_frequency(s1, 1)
	claim = ngram["j"] == 1 and ngram["o"] == 1 and ngram["h"] == 1 and ngram["n"] == 2 and ngram["y"] == 1 and len(ngram) == 5
	return assertion(claim,
		"Passed ngram_5",
		"Failed ngram_5: frequency count was" + str(ngram))

def test_ngram_06():
	s1 = "johnny"
	ngram = ngram_frequency(s1, 2)
	claim = ngram["jo"]==1 and ngram["oh"]==1 and ngram["hn"]==1 and ngram["nn"]==1 and ngram["ny"]==1 and len(ngram)==5
	return assertion(claim,
		"Passed ngram_6",
		"Failed ngram_6: frequency count was " + str(ngram))

def test_ngram_07():
	s1 = "john"
	ngram = ngram_frequency(s1, 1, normed=True)
	claim = ngram["j"]==0.25 and ngram["o"]==0.25 and ngram["h"]==0.25 and ngram["n"]==0.25 and len(ngram)==4
	return assertion(claim,
		"Passed ngram_7",
		"Failed ngram_7: prob count was " + str(ngram))

def test_ngram_08():
	s1 = "john"
	ngram = ngram_frequency(s1, 2, normed=True)
	third = 1.0 / 3
	claim = accurate(ngram["jo"], third) and accurate(ngram["oh"],third) and accurate(ngram["hn"],third) and len(ngram)==3 and accurate(sum(ngram.values()), 1.0)
	return assertion(claim,
		"Passed ngram_8",
		"Failed ngram_8: prob count was " +  str(ngram))

def test_ngram_09():
	words = ["johnny", "halal", "abdul", "aziz", "ansari", "muhammad", "assyria", "chaldean", "armenian", "van", "elias", "judah", "judea", "zion", "gonder", "ethiopia", "solomon", "chechen", "brezhnev"]
	ngram = ngram_frequency(words, 2, normed=True)
	claim = accurate(sum(ngram.values()), 1.0)
	return assertion(claim,
		"Passed ngram_9",
		"Failed ngram_9: sum of prob counts was " + str(sum(ngram.values())) + " instead of 1.0")

def test_ngram_10():
	words = ["andy", "warhol"]
	ngram = ngram_frequency(words, 2, normed=True)
	eighth = 1.0 / 8
	claim = accurate(ngram["an"],eighth) and accurate(ngram["nd"],eighth) and accurate(ngram["dy"],eighth) and accurate(ngram["wa"],eighth) and accurate(ngram["ar"],eighth) and accurate(ngram["rh"],eighth) and accurate(ngram["ho"],eighth) and accurate(ngram["ol"],eighth) and len(ngram)==8 and accurate(sum(ngram.values()), 1.0)
	return assertion(claim,
		"Passed ngram_10",
		"Failed ngram_10: for some reason")

def test_smoothing_01():
	alphabet = get_ngram_alphabet("alpha", 1)
	s = "john"
	distribution = ngram_frequency(s, 1, normed=False, smoothing=True, alphabet=alphabet)
	all_chars_in_dist = reduce(lambda x,y : x and y, [char in distribution for char in alphabet])
	counts_correct = distribution["j"]==2 and distribution["o"]==2 and distribution["h"]==2 and distribution["n"]==2
	claim = all_chars_in_dist and counts_correct
	return assertion(claim,
		"Passed smoothing_01",
		"Failed smoothing_01: smoothed? "+str(all_chars_in_dist)+", counts correct? "+str(counts_correct))

def test_smoothing_02():
	alphabet = get_ngram_alphabet("alpha", 1)
	s = "john"
	distribution = ngram_frequency(s, 1, normed=True, smoothing=True, alphabet=alphabet)
	claim = reduce(lambda x,y : x and y, [distribution[x] > 0 for x in alphabet])
	return assertion(claim,
		"Passed smoothing_02",
		"Failed smoothing_02: some character has a non-positive probability")

def test_smoothing_03():
	alphabet = get_ngram_alphabet("alpha", 2)
	s = "johnny"
	distribution = ngram_frequency(s, 2, normed=True, smoothing=True, alphabet=alphabet)
	claim = reduce(lambda x,y : x and y, [distribution[x] > 0 for x in alphabet])
	return assertion(claim,
		"Passed smoothing_03",
		"Failed smoothing_03: some character has a non-positive probability")

def test_bhattacharyya_01():
	alphabet = ["h","e","l","l","o","i","n"]
	d1 = ngram_frequency("hello", 1, normed=True)
	d2 = ngram_frequency("hellion", 1, normed=True)
	claim = bhattacharyya(d1,d2,alphabet) == bhattacharyya(d2,d1,alphabet)
	return assertion(claim,
		"Passed bhattacharyya_01",
		"Failed bhattacharyya_01: d(p,q) should be equal to d(q,p)")

def test_bhattacharyya_02():
	alphabet = ["h","e","l","o"]
	d1 = ngram_frequency("hello", 1, normed=True)
	distance = bhattacharyya(d1,d1,alphabet)
	claim = distance == 0
	return assertion(claim,
		"Passed bhattacharyya_02",
		"Failed bhattacharyya_02: d(p,p) should be equal to 0 but it was "+str(distance))

def test_bhattacharyya_03():
	alphabet = [""]
	d1 = ngram_frequency("", 1, normed=True)
	claim = bhattacharyya(d1,d1,alphabet) == 0
	return assertion(claim,
		"Passed bhattacharyya_03",
		"Failed bhattacharyya_03: distance between empty prob distributions is zero")

def test_bhattacharyya_04():
	alphabet = set([char for char in "wellington"] + [char for char in "hamilton"])
	d1 = ngram_frequency("wellington", 1, normed=True)
	d2 = ngram_frequency("hamilton", 1, normed=True)
	bd = bhattacharyya(d1,d2,alphabet)
	return assertion(accurate(bd, 0.42826, 0.0001),
		"Passed bhattacharyya_04",
		"Failed bhattacharyya_04: distance should be 0.42826266... but it was " + str(bd))

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