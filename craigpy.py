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


# In[20]:

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
