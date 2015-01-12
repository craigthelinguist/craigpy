import pycountry as __pc__
import ling
import itertools
from functools import reduce

def get_tld(domain, FQDN=True):
	'''
	Given a domain name, return the top-level part.

	Parameters
	----------
		domain : str
			domain-name to get the tld of.
		FQDN : bool
			is the domain name fully qualified? i.e.: does it end with "."
	'''
	domain = domain.split(".")
	return domain[-2] if FQDN else domain[-1]

def get_sld(domain, FQDN=True):
	'''
	Given a domain name, return the second-level part.


	Parameters
	----------
		domain : str
			domain-name to get the sld of.
		FQDN : bool
			is the domain name fully qualified? i.e.: does it end with "."
	'''
	domain = domain.split(".")
	return domain[-3] if FQDN else domain[-2]

def get_country(countrycode, official_name=False):
	'''
	Given a country code, return the corresponding country.

	Parameters
	----------
		countrycode : str
			the countrycode you want to look up, e.g.: "DE" for Germany

	Keyword Arguments
	-----------------
		official_name : bool
			if true, return the countries official name ("Federal Republic of Germany")
			if false, returns a shorter name ("Germany")
	'''
	countrycode = countrycode.upper()
	return __pc__.countries.get(alpha2=countrycode).name

def KL_divergence(test_domains, good_domains, botnet_domains, degree, alphabet="alphanumeric"):
	'''
	Perform the symmetric Kullback-Leibler divergence test on the given test domains.

	Parameters
	----------
		test_domains : Iterable
			collection of domains you want to test with Kullback-Leibler divergence
		good_domains : Iterable
			collection of domains known to be legitimate
		botnet_domains : Iterable
			collection of domains known to be algorithmically generated
		degree : int
			degree of n-grams to tests (e.g.: unigrams = 1, bigrams = 2)
			should be a positive integer

	Keyword Arguments
	-----------------
		alphabet : "alpha" or "numeric" or "alphanumeric"
			possible chars
	'''

	# create alphabet
	chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
			 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
	if alphabet == "alpha":
		alphabet = chars
	elif alphabet == "numeric":
		alphabet = nums
	elif alphabet == "alphanumeric":
		alphabet = chars + nums

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

	# get distribution for a collection of words
	def get_dist(words):
		main_dist = {}
		for string in words:
			word_dist = ling.ngram_frequency(string, degree, True)
			for key in word_dist:
				if key not in main_dist:
					main_dist[key] = 0
				main_dist[key] = main_dist[key] + 1
		for key in main_dist:
			main_dist[key] = 1.0 * main_dist[key] / len(words)
	dist_good = get_dist(good_domains)
	dist_botnet = get_dist(botnet_domains)
	dist_test = get_dist(test_domains)

	# a symmetric measure of distance
	def symmetric_divergence(d1, d2):
		return 0.5 * (ling.kullback_leibler(d1,d2) + ling.kullback_leibler(d2,d1))

	# compare distance between test distribution and the good/bad distributions
	d_qg = symmetric_divergence(dist_test, dist_good)
	d_qb = symmetric_divergence(dist_test, dist_botnet)
	result = d_qg - d_qb
	return result > 0
