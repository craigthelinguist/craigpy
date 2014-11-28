from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from matplotlib import patches as mpatches
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

def interactive_legend(ax,names,colours):
    ''' create and return an interactive legend for the specified axis. You can click on legends to hide/show the corresponding series.
            ax: axis for which you are creating the interactive legend.
            names: list of names for the legend keys.
            colours: list of colours for the legend keys. '''
    
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
        fig.canvas.draw()
    
    # activate pick event for legend on the figure
    fig = ax.get_figure()
    fig.canvas.mpl_connect("pick_event", onpick_legends)
    return leg