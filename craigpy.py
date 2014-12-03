
# coding: utf-8

# In[3]:

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from matplotlib import patches as mpatches
import matplotlib
import matplotlib.pyplot as plt
import math

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

def plot_barchart_from_series(series, normed=True, autoformat=True):
    ''' plot the given series as a barchart.
            normed : plot as a % of all the values
            autoformat : if you are norming, autoformat will scale the y-axis accordingly
        returns the axis being plotted on '''
    
    # norm everything if needed
    if normed:
        counts = {}
        total_sum = reduce(lambda x,y : x+y, series)
        for country in series.index:
            count = series[country]
            avged = count*1.0 / total_sum
            counts[country] = avged
        series_normed = Series(counts)
        series_normed.order(ascending=False,inplace=True)
        
    if normed:
        ax = series_normed.plot(kind="bar")
        if autoformat:
            ax.set_ylim(0)
            ax.set_yticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    else:
        ax = series.plot(kind="bar")
    return ax

def interactive_legend(ax,names,colours, autoscale=False):
    ''' create and return an interactive legend for the specified axis. You can click on legends to hide/show the corresponding series.
            ax: axis for which you are creating the interactive legend.
            names: list of names for the legend keys.
            colours: list of colours for the legend keys.
            autoscale : if you hide/show series, whether the graph will readjust the scale
                of the y-axis. '''
    
    # make legend keys
    patches = [ mpatches.Patch(facecolor=colours[i], edgecolor="black", linewidth=2.0, label=names[i])
                for i in range(len(names)) ]
    
    # legend formatting
    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5,1.05),
                    ncol=5, fancybox=True, shadow=True, handles=patches)
    
    # make a mapping of legend -> line
    linemap = {}
    lines = ax.get_lines()
    patches = leg.get_patches()
    for patch, line in zip(patches, lines):
        patch.set_picker(5)
        linemap[patch] = line
    
    # function to use for rescaling
    def rescale(ax):
        ''' rescales y axis to accommodate all data
            changes the y ticks to be a bit nicer as well
                df: the data
                ax: axis on which the data is being plotted
                lines: list of the series that are plotted  '''
        # find largest value being plotted  
        mx = max([line.get_ydata().max() for line in lines if line.get_visible()])
        mx = mx * 1.1 # put a little bit of space above the maximum
        step = mx/6.0
        ticks = [ round(step*i/1000) * 1000 for i in range(6) ]
        ax.yaxis.set_ticks(ticks)
        plt.ylim(0,mx)
        
    # create pick event for legend
    def onpick_legends(event):
        ''' a pick event for legend
            when you click a legend it toggles visibility for the corresponding series '''
        patch = event.artist
        line = linemap[patch]
        vis = not line.get_visible()
        line.set_visible(vis)
        if vis:
            patch.set_alpha(1.0)
        else:
            patch.set_alpha(0.4)
        if autoscale:
            rescale(ax)
        fig.canvas.draw()
    
    
    # activate pick event for legend on the figure
    fig = ax.get_figure()
    fig.canvas.mpl_connect("pick_event", onpick_legends)
    
    return leg

def load_cc(fname):
    ''' load country codes from given filename; return a dict of cc -> country name '''
    codes = {}
    f = open(fname)
    for line in f:
        line = line.split(",")
        cc = line[0]
        country = line[1].rstrip()
        codes[cc] = country
    return codes

def normed_series(series,order=True,ascending=False):
    ''' given a series returns a series with all the values normalised
        args:
            series : the series you want to normalise
        kargs:
            order : whether the series that is returned should be sorted
            ascending : if sorting, how the series should be sorted.
        return:
            series : a normalised series
    '''
    counts = {}
    total_sum = reduce(lambda x,y : x+y, series)
    for indx in series.index:
        count = series[indx]
        normed = count*1.0 / total_sum
        counts[indx] = normed
    series = Series(counts)
    if order:
        if ascending:
            series.order(ascending=True,inplace=True)
        else:
            series.order(ascending=False,inplace=True)
    return series

def parse_yyyymmdd(x):
    ''' take a string x of the form yyyymmdd and return the corresponding datetime64 object '''
    return np.datetime64(x[0:4] + "-" + x[4:6] + "-" + x[6:8])

def load_words(fname):
    ''' load a newline-delimited file of words into a list, return the list '''
    f = open(fname,"r")
    words = []
    for line in f:
        line = line.rstrip()
        words.append(line)
    f.close()
    return words

def save_words(fname, words):
    ''' save elements in words to a new file called fname
        the elements are delimited by a newline '''
    f = open(fname,"w")
    for word in words:
        f.write(word + "\n")
    f.close()


# In[3]:




# In[15]:




# In[1]:




# In[17]:




# In[9]:




# In[2]:




# In[ ]:



