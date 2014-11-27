from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot_barchart(df, dates, normed=True, autoformat=True):
    ''' plot the columns of df in a barchart. assumes df is indexed with datetime objects.
            df : data to plot
            dates : a dict of str -> array[datetime] objects. arrays of datetime objects will
                be plotted together, using str to identify them. If None, all data will be
                plotted in one group.
            normed : plot as a % of all the values
            autoformat : if you are norming, autoformat will scale the y-axis accordingly.
        returns the axis being plotted on '''
    
    # this lambda returns the subset of df that contains the dates in the specified array
    subset = lambda df,dates : df.ix[[df.index[x] for x in range(len(df.index)) if df.index[x] in dates]]
    subsets = {}
    
    # create the subsets and norm them
    for name, datelist in dates.items():
        if dates:
            sub = subset(df,datelist)
            counts = { col : sub[col].mean() for col in sub }
        if normed:
            values_to_sum = [x for x in counts.itervalues() if not np.isnan(x)]
            total_count = reduce(lambda x,y : x+y, values_to_sum)
            counts = { key : value/total_count for key,value in counts.iteritems() }
        subsets[name] = counts

    # create a dataframe appropriate for plotting
    barchart_df = DataFrame(subsets)
    
    # plot, autoformat, return
    ax = barchart_df.plot(kind="bar")
    if autoformat and normed:
        ax.set_ylim(0)
        ax.set_yticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    return ax
