import pycountry as __pc__
import ling
import socket

__slds__ = ["ac", "co", "geek", "gen", "kiwi", "maori", "net", "org", "school", "cri", "govt", "gov", "health", "iwi", "mil", "parliament"]
__ccs__ = [country.alpha2.lower() for country in __pc__.countries] + [country.alpha2.lower() for country in __pc__.historic_countries]
__tlds__ = ["com", "net", "org", "int", "edu", "gov", "mil", "arpa", "biz"] + __ccs__

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
	if domain[-1] == "": # get rid of root
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

def country_from_cc(countrycode, official_name=False):
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
	if stripped[-1] in __tlds__: # first-level domain
		stripped = stripped[:-1]
	if stripped[-1] in __slds__: # second-level domain
		stripped = stripped[:-1]
	return ".".join(stripped)

def does_domain_resolve(domain):
	'''
	Check if the given domain resolves to an IP address.
	Return : bool

	Parameters
	----------
		domain : str
			domain name to check
	'''
	try:
		socket.gethostbyname(domain)
		return True
	except socket.gaierror:
		return False

def ip_from_domain(domain):
	'''
	Return the IP address of the given domain.
	Return None if there isn't one.
	'''
	try:
		return socket.gethostbyname(domain)
	except socket.gaierror:
		return None


def is_valid(domain):
	'''
	Return true if the domain has a valid name.
	'''
	domain = strip_hld(domain.lower()).split(".")[-1]

	# check for improper length
	if len(word) < 2:
		return False

	# cannot begin or end with a hyphen
	if word[0] == "-" or word[-1] == "-":
		return False

	# check for illegal characters
	for char in word:
		if char not in __validchars__:
			return False

	return Trued
