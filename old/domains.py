import craigpy as cp
import pandas as pd
from pandas import Series
from pandas import DataFrame
import linguistics as ling
import math as math

def filter_domains_by_corpus(dataframe, corpus, domain="hld"):
    ''' filter the "domain" column of the specified data frame. Remove those entries whose domain is
        not contained in the corpus.
            domain : either hld or sld. If hld, will check the higher-level domain name against the
                    corpus. If sld, will check the lower-level domain name against the corpus. '''
    if domain == "hld":
        func = lambda name : "".join(name.split(".")[:-4]) in corpus
    else:
        func = lambda name : ".".join(name.split(".")[-4:])[:-1] in corpus
    mask = dataframe["domain"].map(func)
    return dataframe[mask]

def filter_column(dataframe, column, corpus):
    ''' filter dataframe by column. Removes those entries in column that are not in corpus.
        e.g.: let column = "country", and let corpus be a set of countries
            dataframe : dataframe you want to filter
            column : column that you want to filter by
            corpus : entries that you are interested in '''
    func = lambda name : name in corpus
    mask = dataframe[column].map(func)
    return dataframe[mask]

def filter_domains(dataframe, words, substrings, filtering="hld", entropy=None):
    ''' filter the "domain" column in the specified dataframe. Remove any rows where:
            - the name is contained in the list of words.
            - there is a substring in substrings contained in the name.
            - the name's entropy is lower than the specified entropy threshold.
        key arguments:
            filtering : either "hld" or "sld". If "hld", then filter by the high-level part of the domain.
                if "sld" then filter by the second-level part of the domain
            entropy : either None or a value between 0 and 1. If a value between 0 and 1, this is used as a
                threshold. If the name has entropy lower than the specified threshold, it will be filtered. '''
    
    # specify which part of the domain you should be filtering
    if filtering == "hld":
        nameparse = lambda name : "".join(name.split(".")[:-4])
    elif filtering == "sld":
        nameparse = lambda name : ".".join(name.split(".")[-4:])[:-1]
    else:
        return None
    
    # define a function for filtering
    def word_filter(name):
        ''' filter the given string. Returns "true" if the string should be included, "false" if the string should
            be removed/if the string should be filtered '''
        name = nameparse(name)
        if entropy:
            entropy_score = ling.entropy(name)
            if entropy_score < entropy:
                return False
        if name in words:
            return False
        for substr in substrings:
            if substr in name:
                return False
        return True

    # create boolean vector, mask the dataframe, return
    mask = dataframe["domain"].map(word_filter)
    return dataframe[mask]

# count of all queries
def summary_hlds(dataframe, queries="all", top="all"):
    ''' aggregate the entries of dataframe, grouping by the higher-level domain name. Returns a mapping
        of hld -> count.
            dataframe : data you want to summarise
            queries : hld's that you are interested in, if you want a subset ("all" by default)
            top : if you specify a number x, return only the x most frequent results '''
    counts={}
    for domain in df[:]["domain"]:
        names = domain.split(".")
        sld = ".".join(names[-4:])
        sld = sld[:-1] # get rid of root
        names = names[:-4]
        name = ".".join(names)
        if queries == "all" or name in queries:
            if name in counts:
                counts[name] = counts[name] + 1
            else:
                counts[name] = 1
    series = Series(counts)
    series.sort(ascending=False)
    if top != "all":
        series = series[:top]
    return series
