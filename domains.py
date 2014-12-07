import craigpy as cp
import pandas as pd
from pandas import Series
from pandas import DataFrame

def filter_queries_hld(dataframe, corpus):
    ''' filter dataframe by words in corpus. Removes those entries whose higher-level domain name is not in the supplied
        corpus.
            dataframe : dataframe you want to filter
            corpus : higher-level domain names that you are interested in '''
    func = lambda name : "".join(name.split(".")[:-4]) in corpus
    mask = dataframe["domain"].map(func)
    return dataframe[mask]

def filter_queries_sld(dataframe, corpus):
    ''' filter dataframe by words in corpus. Removes those entries whose second-level domain name is not in the supplied
        corpus.
            dataframe : dataframe you want to filter
            corpus : second-level domain names that you are interested in '''
    func = lambda name : ".".join(name.split(".")[-4:])[:-1] in corpus
    mask = dataframe["domain"].map(func)
    return dataframe[mask]

def filter_queries_custom(dataframe, column, corpus):
    ''' filter dataframe by column. Removes those entries in column that are not in corpus.
        e.g.: let column = "country", and let corpus be a set of countries
            dataframe : dataframe you want to filter
            column : column that you want to filter by
            corpus : entries that you are interested in '''
    func = lambda name : name in corpus
    mask = dataframe[column].map(func)
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

