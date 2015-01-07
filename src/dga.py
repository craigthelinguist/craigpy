import pycountry as __pc__

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