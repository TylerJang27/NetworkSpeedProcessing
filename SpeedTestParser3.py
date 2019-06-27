# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:16:26 2019

@author: tajgo
@author: cyberpizza team
Some code for graphing and calculating statistics taken from https://pundit.pratt.duke.edu/wiki/
Date graphing and filling taken from https://stackoverflow.com/questions/29329725/pandas-and-matplotlib-fill-between-vs-datetime64/29329823#29329823
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.dates import DateFormatter
from matplotlib.dates import datetime as dt ###
from scipy.interpolate import spline
import dateutil.parser

# %% Prepare data   
# Load data from Sample_to_parse.txt
speed_data = np.loadtxt('sample_to_parse.txt', skiprows=4, usecols=(4,5,7)) #missing date ()
# Copy data from each column into new variables
down_speed = speed_data[:, 0].copy()
down_speed = down_speed / 1000000
up_speed = speed_data[:, 1].copy()
up_speed = up_speed / 1000000
latency = speed_data[:, 2].copy()
num_points=500
num_points2=(int)(num_points * (down_speed.size-1)/down_speed.size)
time_of_test=np.arange(0, (int)(down_speed.size), 1)
time_model = np.linspace(np.min(time_of_test), np.max(time_of_test), num_points2)

# Read dates
f=open('sample_to_parse.txt', 'r')
lines = f.readlines()
time_data = []
time_of_test1 = []
time_of_test2 = []
for x in range(4, len(lines) - 1):
    time_data.append((lines[x][100:126]))
    new_date=dateutil.parser.parse(lines[x][100:126])
    time_of_test1.append(new_date)
    #time_of_test2.append(new_date.year * 10000000000 + new_date.month * 100000000 + new_date.day * 1000000 + new_date.hour * 10000 + new_date.minute * 100 + new_date.second)
f.close()


# %% Generate estimates and model
down_model = spline(time_of_test,down_speed,time_model)
up_model = spline(time_of_test,up_speed,time_model)
lat_model = spline(time_of_test,latency,time_model)

# %% Calculate data and statistics
up_avg = np.mean(up_speed)
down_avg = np.mean(down_speed)
lat_avg = np.mean(latency)

# %% Format data with pandas

oldest = min(time_of_test1)
youngest = max(dt for dt in time_of_test1)
date_model = pd.date_range(oldest, youngest, periods=num_points2)
data = pd.DataFrame({'Download': down_model, 'Upload': up_model, 'Latency': lat_model, 'Time': date_model})
multiplier = (int)(num_points2/len(time_data))
time_stretch = [val for val in time_of_test1 for _ in range(multiplier)]
down_stretch = [val for val in down_speed for _ in range(multiplier)]
up_stretch = [val for val in up_speed for _ in range(multiplier)]
lat_stretch = [val for val in latency for _ in range(multiplier)]
msize=10
name1="Download Speed"
name2="Upload Speed"
name3="Latency"
for k in time_of_test1:
    time_of_test2.append(k.strftime('%m/%d %H:%m'))

# %%Plot Graphs of Data
fig, axs = plt.subplots(2, 1,figsize=(10, 10))
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
fig.subplots_adjust(hspace=0.5)
plt.subplot(211)
fig.suptitle("Internet Speeds Over Last Week", fontsize=30)
plt.grid(False)

#Download and Upload Speed
plt.plot_date(time_stretch, down_stretch, 'bo', markevery=multiplier, ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
plt.plot_date(time_stretch, up_stretch, 'ro', markevery=multiplier, ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
#plt.plot_date(data['Time'], data['Download'], 'b-')
#plt.plot_date(data['Time'], data['Upload'], 'r-')

#Shading
d = data['Time'].values
plt.fill_between(d, data['Download'], data['Upload'], where=data['Download'] >= data['Upload'],facecolor='dodgerblue', alpha=0.9, interpolate=True)
plt.fill_between(d, data['Download'] - 0.65, data['Upload'], where=data['Download']-0.65 >= data['Upload'],facecolor=(0.05, 0.50, 0.9), alpha=0.9, interpolate=True)

plt.fill_between(d, data['Upload'], y2=0, where=data['Download'] >= data['Upload'],facecolor='salmon', alpha=0.9, interpolate=True)
plt.fill_between(d, data['Upload'] - 0.65, y2=0, where=data['Download'] >= data['Upload'],facecolor=(.90, .50, .50), alpha=0.9, interpolate=True)


plt.fill_between(d, data['Download'], data['Upload'], where=data['Download'] < data['Upload'],facecolor='salmon', alpha=0.9, interpolate=True)
#plt.fill_between(d, data['Download'] - 0.75, data['Upload'], where=data['Download'] < data['Upload'] - 0.65,facecolor=(0.9, 0.5, 0.5), alpha=0.9, interpolate=True)

plt.fill_between(d, data['Download'], y2=0, where=data['Download'] < data['Upload'],facecolor='dodgerblue', alpha=0.9, interpolate=True)
plt.fill_between(d, data['Download'] - 0.65, y2=0, where=data['Download'] < data['Upload'],facecolor=(0.05, 0.5, 0.9), alpha=0.9, interpolate=True)

plt.fill_between(d, data['Upload'] - 0.65, data['Download'], where=data['Download'] < data['Upload'] - 0.65,facecolor=(0.9, 0.5, 0.5), alpha=0.9, interpolate=True)


blue_patch = mpatches.Patch(color='blue', label=name1)
red_patch = mpatches.Patch(color='red', label=name2)
plt.xlabel("Time", fontsize=20)
plt.ylabel("Speed (Mbps)", fontsize=20)
plt.figlegend([blue_patch, red_patch], ('Download', 'Upload'), loc=(0.75, 0.81), fancybox=True, framealpha=0.8, shadow=True, fontsize=15)

plt.xticks(rotation=25, color="k")
plt.xticks(time_of_test1, time_of_test2)

#Latency Plot
plt.subplot(212)
plt.plot_date(time_stretch, lat_stretch, 'go', markevery=multiplier, ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
plt.fill_between(d, data['Latency'], y2=0, facecolor='mediumseagreen', alpha=0.9, interpolate=True)
plt.fill_between(d, data['Latency'] - 7, y2=0, facecolor=(0.2, 0.65, 0.4), alpha=0.9, interpolate=True)

plt.xlabel("Time", fontsize=20)

plt.xticks(rotation=25, color="k")
plt.xticks(time_of_test1, time_of_test2)
plt.ylabel("Latency (ms)", fontsize=20)

# %% Save and show figure
plt.savefig('net_speed_plot.png')
plt.show()

