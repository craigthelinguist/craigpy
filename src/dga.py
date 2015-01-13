import pycountry as __pc__
import ling

__slds__ = ["ac", "co", "geek", "gen", "kiwi", "maori", "net", "org", "school", "cri", "govt", "health", "iwi", "mil", "parliament"]

def get_tld(domain):
	'''
	Given a domain name, return the top-level part.

	Parameters
	----------
		domain : str
			domain-name to get the tld of.
	'''
	domain = domain.split(".")
	return domain[-2] if domain[-1] == "" else domain[-1]

def get_sld(domain):
	'''
	Given a domain name, return the second-level part.

	Parameters
	----------
		domain : str
			domain-name to get the sld of.
	'''
	domain = domain.split(".")
	if domain[-1] == "":
		domain = domain[:-1]
	if domain[-1] != "nz":
		return ""
	if domain[-2] not in __slds__:
		return ""
	else:
		return domain[-2]

def get_lld(domain):
	'''
	Given a domain name, return the lowest-level part.
	E.g.: "hello.world.org.nz. --> "hello"
	
	Parameters
	----------
		domain : str
			domain whose lowest-level domain name you want
	'''
	return domain.split(".")[0]

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

def strip_hld(domain):
	'''
	Given a domain name in the .nz namespace, return that domain-name with the top-level and second-level parts stripped.
	
	Parameters
	----------
		domain : str
			a domain name in the .nz namespace
	'''
	stripped = domain.split(".")
	if len(stripped) == 0:
		return ""
	if stripped[-1] == "": # get rid of root
		stripped = stripped[:-1]
	if len(stripped) < 2:
		return ""
	if stripped[-1] == "nz": # first-level domain
		stripped = stripped[:-1]
	if stripped[-1] in __slds__: # second-level domain
		stripped = stripped[:-1]
	return ".".join(stripped)

def get_alphabet(alphabet="alphanumeric", degree):

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

	return ngrams

def KL_test(test_distribution, good_distribution, botnet_distribution, degree, alphabet="alphanumeric"):
	'''
	Perform the symmetric Kullback-Leibler divergence test on the given test domains.
	Return true if the test_distribution is closer to the botnet_distribution than to the good_distribution.

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

	# get distributions for each collection
	dist_good = get_dist(good_domains)
	dist_botnet = get_dist(botnet_domains)
	dist_test = get_dist(test_domains)

	# compare distance between test distribution and the good/bad distributions
	d_qg = ling.kullback_leibler_distance(dist_test, dist_good, degree, alphabet)
	d_qb = ling.kullback_leibler_distance(dist_test, dist_botnet, degree, alphabet)
	return d_qg > d_qb