from decimal import Decimal
import math as __math__
from collections import Iterable

def get_ngram_alphabet(characters, degree):
	'''
	Given a collection of unigrams and a degree n, returns the set of all n-grams.

	Parameters
	----------
	characters : "alpha", "numeric", "alphanumeric", or Iterable
		a collection of unigrams
	degree : int >= 1
		degree of n-grams to compute
	'''

	# check arguments
	if degree < 1:
		raise ValueError("Degree must be >= 1")

	# create unigram alphabet
	chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
			 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
	alphabet = None
	if characters == "alpha":
		alphabet = chars
	elif characters == "numeric":
		alphabet = nums
	elif characters == "alphanumeric":
		alphabet = chars + nums
	elif not isinstance(characters, Iterable):
		raise TypeError("characters must be Iterable or 'alpha', 'numeric', or 'alphanumeric'")
	else:
		alphabet = characters

	# get all possible n-grams
	def product(a, b):
		results = []
		for c1 in a:
			for c2 in b:
				results.append(c1 + c2)
		return results
	ngrams = alphabet
	for i in range(degree-1):
		ngrams = product(ngrams, alphabet)

	return ngrams

def levenshtein(string1, string2, case_sensitive=False,
				insertion=1, deletion=1, skip=0, transform=1):
	'''
	Compute the Levenshtein distance between two strings.
	Returns int

	Operations:
	------------------
		insertion : int
			insert a character into string A
			default: 1
		deletion : int
			delete character at string A
			default: 1
		skip : int
			do nothing to current characters of string A and be
			default: 0
		transform : int
			transform A's character into B's character
			default: 1

	Keyword Arguments:
	------------------
		case_sensitive : bool
			whether uppercase and lowercase chars should be considered the same
	'''
	operations = {
		"deletion" : deletion,
		"insertion" : insertion,
		"skip" : skip,
		"transform " : transform
	}
	return edit_dist(string1, string2, operations, case_sensitive, minimise=True)

def seq_align(str1, str2, case_sensitive=False,
			  match=1, mismatch=-1, skip=-2):
	'''
	Compute the score of the optimal sequence alignment of two strings.

	Operations:
	-----------
		match : int
			cost of matching two of the same characters
			default: 1
		mismatch : int
			cost of matching two different characters
			default: -1
		skip : int
			cost of skipping over a string by appending padding
			default: -2

	Keyword Arguments:
	------------------
		case_sensitive : bool
			whether uppercase and lowercase chars should be considered the same
	'''
	operations = {
		"insertion" : skip,
		"deletion" : skip,
		"skip" : match,
		"transform" : mismatch
	}
	return edit_dist(str1, str2, operations, case_sensitive, minimise=False)

def edit_dist(str1, str2, operations, case_sensitive=False, minimise=True):
	'''
	Compute the edit distance between two strings.
	Returns int.

	Parameters:
	-----------
	operations : { str -> int }
		operations to use and their associated cost.
		valid operations: "insertion", "deletion", "transform", "skip".
		must have "insertion" and "deletion"

	Keyword Arguments:
	------------------
	case_sensitive : bool
		Whether to treat uppercase and lowercase characters the same.
		Default: False
	minimise : bool
		Whether we want the highest score, or the lowest score.
		Default: True (lowest score)
	'''

	if "insertion" not in operations or "deletion" not in operations:
		raise KeyError("Edit distance needs costs associated with insertion and deletion operations.")

	if not case_sensitive:
		str1 = str1.lower()
		str2 = str2.lower()

	# init rows
	# use optimisation - we only care about score, so we only need to know last two rows
	rows = len(str1) + 1
	cols = len(str2) + 1
	botrow = [operations["insertion"] * i for i in range(cols)]
	row = 0

	# fill out rows
	for row in range(1,rows):
		toprow = botrow
		botrow = [row * operations["deletion"]] + [0]*(cols-1) # pre-allocate row
		for col in range(1, cols):

			# compute scores for each operation
			scores = []
			if "deletion" in operations:
				score = toprow[col] + operations["deletion"]
				scores.append(score)
			if "insertion" in operations:
				score = botrow[col-1] + operations["insertion"]
				scores.append(score)
			if "transform" in operations and str1[row-1] != str2[col-1]:
				score = toprow[col-1] + operations["transform"]
				scores.append(score)
			if "skip" in operations and str1[row-1] == str2[col-1]:
				score = toprow[col-1] + operations["skip"]
				scores.append(score)

			# get appropriate score
			if minimise:
				score = min(scores)
			else:
				score = max(scores)
			botrow[col] = score

	return botrow[-1]

def alignment(str1, str2, match=1, mismatch=-1, skip=-2, case_sensitive=False, pad_character="_"):
	'''
	Compute the optimal alignment of two strings.
	Returns (str,str).


	Parameters:
	-----------
		str1 : str
			first string to align.
		str2 : str
			second string to align.

	Keyword Arguments:
	------------------
		match : int
			score that should be applied when two identical characters are aligned.
			(default=1)
		mismatch : int
			score that should be applied when two different characters are aligned.
			(default=-1)
		skip : int
			score that should be applied when a character has to be aligned with a skip.
			(default=-2)
		pad_character : str
			character that should be used to represent padding. For example:
				hello		hello
				hell_		_ill_
			(default="_")
		case_sensitive : bool
			whether you should treat uppercase and lowercase chars the same
			(default=False)
	'''

	if not case_sensitive:
		str1 = str1.lower()
		str2 = str2.lower()

	#------------------ helper function
	def matching(c1, c2):
		if (c1 == c2):
			return match
		else:
			return mismatch

	#------------------ init table
	rows = len(str1) + 1
	cols = len(str2) + 1
	table = [[0 for col in range(cols)] for row in range(rows)]

	# fill first row and col with zeroes
	for i in range(cols):
		table[0][i] = skip * i
	for j in range(rows):
		table[j][0] = skip * j

	#------------------ fill out table
	for row in range(1,rows):
		for col in range(1,cols):

			# get scores
			match_score = matching(str1[row-1], str2[col-1]) + table[row-1][col-1]
			skip_str1 = skip + table[row-1][col]
			skip_str2 = skip + table[row][col-1]

			# take largest
			table[row][col] = max(match_score, skip_str1, skip_str2)

	#------------------ recover alignment
	row = rows-1
	col = cols-1
	align1 = ""
	align2 = ""

	# when you're at table[0][0] you've matched everything
	while row != 0 or col != 0:

		# score in current cell came from up, left, or up-left
		score = table[row][col]

		# came from above-left, append char to str1 and str2
		if row > 0 and col > 0 and table[row-1][col-1] + matching(str1[row-1], str2[col-1]) == score:
			row = row - 1
			col = col - 1
			align1 = align1 + str1[row]
			align2 = align2 + str2[col]

		# came from above, append char to str1, space to str2
		elif row > 0 and table[row-1][col] + skip == score:
			row = row - 1
			align1 = align1 + str1[row]
			align2 = align2 + pad_character

		# came from left, append char to str2, space to str1
		elif col > 0 and table[row][col-1] + skip == score:
			col = col - 1
			align1 = align1 + pad_character
			align2 = align2 + str2[col]

		# this shouldn't happen, but just in case it does, let's be explicit....
		else:
			raise IndexError("Something spooky happened while recovering optimal alignment. There is a cosmic logic error with this function.")

	#------------------ return strings
	# this reverses strings.
	# thank you guido :^)
	align1 = align1[::-1]
	align2 = align2[::-1]
	return (align1, align2)

def ngram_frequency(string, degree, normed=False, smoothing=False, alphabet=None):
	'''
	Compute the ngram frequency of the given string.
	Return: dict of str -> int, mapping each n-gram to its count.

	Parameters
	----------
	string : str
		string whose ngram frequency you will count
	degree : int
		the degree of the ngram (1-grams, 2-grams, etc.)

	Keyword Arguments
	-----------------
	normed : bool
		if false, return a dict of str -> count, if true, return a dict of str -> probability
	'''

	# error checking
	if degree < 1:
		raise ValueError("Degree of n-gram frequency must be 1 or greater")
	if smoothing and not alphabet:
		raise TypeError("If you want to smooth you must specify all possible values in the alphabet.")

	# n-gram frequency for one string
	if isinstance(string, str):
		word_freq = __ngram_freq_one__(string, degree)
		if smoothing:
			word_freq = __smooth__(word_freq, alphabet)
		if normed:
			word_freq = __norm__(word_freq)
		return word_freq

	# n-gram frequency for multiple strings
	elif isinstance(string, Iterable):
		strings = string
		dist = {}
		for word in strings:
			word_freq = __ngram_freq_one__(word, degree)
			for key in word_freq:
				if key not in dist:
					dist[key] = word_freq[key]
				else:
					dist[key] += word_freq[key]
		if smoothing:
			dist = __smooth__(dist, alphabet)
		if normed:
			dist = __norm__(dist)
		return dist

	# invalid
	else:
		raise TypeError("Must pass string or iterable to n-gram count")

def __norm__(map):
	count = sum(map.values())
	return { key : 1.0 * map[key] / count for key in map }

def __smooth__(map, alphabet):
	'''
	Perform Laplace smoothing on the given map (add one to all possible values in the alphabet).
	'''
	smoothed = {}
	for ngram in alphabet:
		if ngram in map:
			smoothed[ngram] = map[ngram] + 1
		else:
			smoothed[ngram] = 1
	return smoothed

def __ngram_freq_one__(string, degree):
	if degree > len(string):
		return {}
	dist = {}
	for i in range(len(string) - degree + 1):
		s = ""
		for j in range(i,i+degree):
			s = s + string[j]
		if s not in dist:
			dist[s] = 0
		dist[s] = dist[s] + 1
	return dist

def ngram_set(string, degree):
	'''
	Return the set of unique n-grams in the given string.

	Parameters
	----------
	string : str
		string to check
	degree : int
		degree of n-grams to check
	'''
	if degree < 1:
		raise TypeError("Degree of n-gram set must be 1 or greater")
	elif degree > len(string):
		return set([])
	ngrams = set([])
	for i in range(len(string) - degree + 1):
		s = ""
		for j in range(i, i+degree):
			s = s + string[j]
		ngrams.add(s)
	return ngrams

def jaccard(string1, string2, ngram_degree=2):
	'''
	Compute the Jaccard index between two strings.

	Parameters
	----------
	string1 : str
		first string to compare
	string2 : str
		second string to compare

	Keyword Arguments
	-----------------
	ngram_degree : int
		whether to compare unigrams, bigrams, etc.
		default = 2 (compare bigrams)
		should be a positive number
	'''
	dist1 = ngram_set(string1, ngram_degree)
	dist2 = ngram_set(string2, ngram_degree)
	intersection = 1.0 * len(dist1.intersection(dist2))
	union = 1.0 * len(dist1.union(dist2))
	return 1 if union == 0 else intersection / union

def kullback_leibler(dist1, dist2, alphabet):
	'''
	Compute the Kullback-Leibler divergence from dist1 to dist2.
	This is the number of additional bits required to encode dist1 given an optimal encoding for dist2.

	Parameters
	----------
	dist1, dist2 : { str : float }
		frequency distributions to be compared. should map each observation to its probability
	alphabet : Iterable
		all possible values that the observations in the distributions could have taken on.
		for example, if you're comparing strings by their bigrams, this should be every possble bigram.

	Properties
	----------
	- KL(p,q) =/= KL(q,p)
	- KL(p,q) >= 0
	'''
	alphabet = [x.lower() for x in alphabet]
	divergence = 0
	for ngram in alphabet:
		f1 = dist1[ngram] if ngram in dist1 else 0
		f2 = dist2[ngram] if ngram in dist2 else 0
		if f2 == 0 and f1 != 0:
			raise ValueError("When computing KL(P,Q), Q_i=0 must imply P_i=0!")
		if f1 != 0 and f2 != 0:
			divergence = divergence + f1 * __math__.log(1.0 * f1 / f2)
	return divergence

def kullback_leibler_distance(dist1, dist2, alphabet):
	'''
	Compute Kullback-Leibler distance from dist1 to dist2.
	This is the average of the Kullback-Leibler divergence from dist1 to dist2, and dist2 to dist1.

	Parameters
	----------
	dist1, dist2 : {str : float}
		probability distributions for the n-grams of two strings
	alphabet : Iterable
		all possible n-grams

	Properties
	----------
	- KLD(p,q) = KLD(q,p)
	'''
	return 0.5 * (kullback_leibler(dist1, dist2, alphabet) + kullback_leibler(dist1, dist2, alphabet))


def bhattacharyya(dist1, dist2, alphabet):
	'''
	Compute the Bhattacharyya distance between dist1 and dist2.

	Parameters
	----------
	dist1, dist2 : {str : float}
		probability distributions for the n-grams of two strings
	alphabet : Iterable
		all possible n-grams

	Properties
	----------
	- B(p,q) = B(q,p)
	- B(p,q) = 0 means either p=q or p and q have no elements in common

	Traps
	-----
	- The alphabet passed in must not contain duplicates.
	'''
	coefficient = 0
	for ngram in alphabet:
		d1 = dist1[ngram] if ngram in dist1 else 0
		d2 = dist2[ngram] if ngram in dist2 else 0
		coefficient += __math__.sqrt(d1*d2)
	if coefficient == 0:
		return 0
	return -__math__.log(coefficient)