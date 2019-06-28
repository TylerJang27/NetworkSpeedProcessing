# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:16:26 2019

@author: cyberpizza team
Some code for graphing and calculating statistics taken from https://pundit.pratt.duke.edu/wiki/
Date graphing and filling taken from https://stackoverflow.com/questions/29329725/pandas-and-matplotlib-fill-between-vs-datetime64/29329823#29329823
"""
# %% Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter
from scipy.interpolate import spline
import dateutil.parser

# %% Global variables necessary for user customization
data_to_show = 10 ####should be 14 by default once we set it up #already accounted for top-down bottom-up order
label_skipper = data_to_show // 7

# %% Prepare data   
# Load data from Sample_to_parse.txt
speed_data = np.loadtxt('sample_to_parse.txt', skiprows=4, usecols=(4,5,7)) #missing date ()

# Read dates
f=open('sample_to_parse.txt', 'r')
lines = f.readlines()
num_lines=(len(lines)-1)
time_data = []
time_of_test1 = []
time_of_test2 = []

for x in range(num_lines-data_to_show, num_lines):
    time_data.append((lines[x][100:126]))
    new_date=dateutil.parser.parse(lines[x][100:126])
    time_of_test1.append(new_date)
f.close()

# Copy data from each column into new variables
down_speed = speed_data[num_lines-data_to_show-4:num_lines-4, 0].copy()
down_speed = down_speed / 1000000
up_speed = speed_data[num_lines-data_to_show-4:num_lines-4, 1].copy()
up_speed = up_speed / 1000000
latency = speed_data[num_lines-data_to_show-4:num_lines-4, 2].copy()
num_points=1000
num_points2=(int)(num_points * (down_speed.size-1)/down_speed.size)
time_of_test=np.arange(0, (int)(down_speed.size), 1)
time_model = np.linspace(np.min(time_of_test), np.max(time_of_test), num_points2)




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
msize=6
up_c1=(0, 0.33, 0.53)
up_c2=(0.02,0.47,0.69)
down_c1=(0.91, 0.6, 0.14)
down_c2=(1, 0.85, 0.36)
lat_c1=(0.11, 0.39, 0.39)
lat_c2=(0.2, 0.6, 0.6)
lat_c3=(0.1, 0.7, 0.4)
red_c1=(0.78, 0.31, 0)
gray_c1=(0.4, 0.4, 0.4)
gray_c2=(0.87, 0.9, 0.93)

name1="Download Speed"
name2="Upload Speed"
name3="Latency"
for k in time_of_test1:
    time_of_test2.append(k.strftime('%m/%d %H:%m'))

# %%Plot Graphs of Data
fig, axs = plt.subplots(2, 1,figsize=(10, 10))
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
fig.subplots_adjust(hspace=0.4)
plt.subplot(211)
fig.suptitle("Internet Speeds Over Time", fontsize=30, y=0.93)
plt.grid(alpha=0.4)

#Download and Upload Speed
plt.plot_date(data['Time'], data['Upload'], '-', color=up_c1, lw=msize/2, alpha=0.8)
plt.plot_date(data['Time'], data['Download'], '-', color=down_c1, lw=msize/2, alpha=0.5)
plt.plot_date(time_stretch, down_stretch, 'yo', mfc=down_c1, markevery=multiplier, ms=msize)
plt.plot_date(time_stretch, up_stretch, 'bo', mfc=up_c1, markevery=multiplier, ms=msize)


#Shading
d = data['Time'].values
###plt.fill_between(d, data['Download'], data['Upload'], where=data['Download'] >= data['Upload'],facecolor=down_c2, alpha=0.9, interpolate=True)
plt.fill_between(d, data['Download'] - 0.1, y2=0, where=data['Download']-0.1 >= data['Upload'],facecolor=down_c2, alpha=0.4, interpolate=True)
plt.fill_between(d, data['Download'] - 0.1, y2=0, where=data['Download']-0.1 < data['Upload'],facecolor=down_c2, alpha=0.4, interpolate=True)

###plt.fill_between(d, data['Upload'], y2=0, where=data['Download'] >= data['Upload'],facecolor=up_c2, alpha=0.9, interpolate=True)
###plt.fill_between(d, data['Upload'] - 0.65, y2=0, where=data['Download'] >= data['Upload'],facecolor=up_c1, alpha=0.9, interpolate=True)
plt.fill_between(d, data['Upload'] - 0.1, y2=0, where=(True),facecolor=up_c1, alpha=0.6, interpolate=True)


#plt.fill_between(d, data['Download'], data['Upload'], where=data['Download'] < data['Upload'],facecolor=up_c2, alpha=0.9, interpolate=True)
###plt.fill_between(d, data['Download'] - 0.65, y2=0, where=data['Download'] < data['Upload'],facecolor=up_c1, alpha=0.9, interpolate=True)

#plt.fill_between(d, data['Download'] - 0.75, data['Upload'], where=data['Download'] < data['Upload'] - 0.65,facecolor=(0.9, 0.5, 0.5), alpha=0.9, interpolate=True)

#plt.fill_between(d, data['Download'], y2=0, where=data['Download'] < data['Upload'],facecolor=down_c2, alpha=0.9, interpolate=True)
#plt.fill_between(d, data['Download'] - 0.65, y2=0, where=data['Download'] < data['Upload'],facecolor=down_c1, alpha=0.9, interpolate=True)

###plt.fill_between(d, data['Upload'] - 0.65, data['Download'], where=data['Download'] < data['Upload'] - 0.65,facecolor=up_c1, alpha=0.9, interpolate=True)

blue_patch = mpatches.Patch(color=down_c1, label=name1)
red_patch = mpatches.Patch(color=up_c1, label=name2)
plt.xlabel("Time", fontsize=20)
plt.ylabel("Speed (Mbps)", fontsize=20)
plt.figlegend([blue_patch, red_patch], ('Download', 'Upload'), loc=(0.75, 0.81), fancybox=True, framealpha=0.8, shadow=True, fontsize=15)

plt.xticks(rotation=25, color="k")
plt.xticks(time_of_test1[::label_skipper], time_of_test2[::label_skipper])

#Latency Plot
plt.subplot(212)
plt.plot_date(time_stretch, lat_stretch, 'go', mfc=gray_c1, markevery=multiplier, ms=msize)
plt.plot_date(data['Time'], data['Latency'], '-', color=gray_c1, lw=msize/2, alpha=0.75)

plt.fill_between(d, data['Latency'], y2=0, facecolor=gray_c2, alpha=0.95, interpolate=True)
#plt.fill_between(d, data['Latency'] - 7, y2=0, facecolor=lat_c1, alpha=0.9, interpolate=True)

plt.xlabel("Time", fontsize=20)
plt.grid(alpha=0.4)
plt.xticks(rotation=25, color="k")
plt.xticks(time_of_test1[::label_skipper], time_of_test2[::label_skipper])
plt.ylabel("Latency (ms)", fontsize=20)

# %% Save and show figure
plt.savefig('net_speed_plot.png')
plt.show()

