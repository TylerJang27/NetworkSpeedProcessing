# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:19:17 2019

@author: cyberpizza team
Some code for graphing and calculating statistics taken from https://pundit.pratt.duke.edu/wiki/
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.dates import DateFormatter
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
    time_of_test2.append(new_date.year * 10000000000 + new_date.month * 100000000 + new_date.day * 1000000 + new_date.hour * 10000 + new_date.minute * 100 + new_date.second)
f.close()
print(time_of_test1)
print(time_of_test2)

#time_of_test1 = dateutil.parser.parse(time_data)
#time_of_test = speed_data[:, 6].copy()

latency = speed_data[:, 2].copy()
num_points=500
time_of_test=np.arange(0, (int)(down_speed.size), 1);
time_model = np.linspace(np.min(time_of_test), np.max(time_of_test), (int)(num_points * (down_speed.size-1)/down_speed.size))

# %% Generate estimates and model
down_model = spline(time_of_test,down_speed,time_model)
up_model = spline(time_of_test,up_speed,time_model)
lat_model = spline(time_of_test,latency,time_model)

"""
#For calculating r^2 values
yhat_up = yfun(time_of_test, up_pvec)
yhat_down = yfun(time_of_test, down_pvec)
yhat_lat = yfun(time_of_test, lat_pvec)

def calc_stats(y, yhat, to_print=1):
    # Calculate statistics
    st = np.sum((y - np.mean(y))**2)
    sr = np.sum((y - yhat)**2)
    r2 = (st - sr) / st
    if to_print:
        print('st: {:.3e}\nsr: {:.3e}\nr2: {:.3e}'.format(st, sr, r2))
    return st, sr, r2

calc_stats(yhat_down, down_speed)
calc_stats(yhat_up, up_speed)
calc_stats(yhat_lat, latency)
"""

up_avg = np.mean(up_speed)
down_avg = np.mean(down_speed)
lat_avg = np.mean(latency)
#return up_avg, down_avg, latency_avg

# %% Graph plots
name1="Download Speed"
name2="Upload Speed"
name3="Latency"
line_width=2.5
msize=10
plt.style.use("seaborn-pastel")
fig, axs = plt.subplots(2, 1,figsize=(10, 10))
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)


formatter = DateFormatter('%m/%d %H:%m')
"""
plt.xticks(size=10, rotation=40)

fig, ax= plt.subplots()
plt.plot_date(time_of_test1, down_speed)
ax[0].xaxis.set_major_formatter(formatter)
ax[0].xaxis.set_tick_params(rotation=40, labelsize=10)
plt.show()
"""

# %% Subplot 1, Upload and Download Speed
plt.subplot(211)
fig.suptitle('Internet Speeds Over Last Week', fontsize=30)
#Download Speed

plt.plot(time_of_test, down_speed, 'ko', label=name1, mfc='blue', ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
#plt.plot_date(time_of_test1, down_speed, 'ko', xdate=True, label=name1, mfc='blue', ms=msize)

plt.fill_between(time_model, down_model, y2=0, color='dodgerblue', alpha=0.9)
blue_patch = mpatches.Patch(color='blue', label=name1)

#Upload Speed
plt.plot(time_of_test, up_speed, 'ko', label=name2, mfc='red', ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
#plt.plot_date(time_of_test1, up_speed, 'ko', label=name2, mfc='red', ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])

#Filling Operations
fill_boolean=down_model<up_model
fill2_boolean=down_model>=up_model
plt.fill_between(time_model, down_model, y2=up_model, where=fill_boolean, color='salmon')
plt.fill_between(time_model, up_model, y2=down_model, color='dodgerblue', where=fill2_boolean)
plt.fill_between(time_model, up_model, y2=0, where=fill2_boolean, color='salmon', alpha=0.9)
red_patch = mpatches.Patch(color='red', label=name2)
plt.grid(False)
plt.xlabel("Time", fontsize=20)
plt.ylabel("Speed (Mbps)", fontsize=20)
plt.figlegend([blue_patch, red_patch], ('Download', 'Upload'), loc=(0.75, 0.8), fancybox=True, framealpha=0.8, shadow=True, fontsize=15)

axs[0].format_xdata = formatter

# %% Subplot 2, Latency
plt.subplot(212)
plt.plot(time_of_test, latency, 'ko', label=name3, mfc='green', ms=msize, path_effects=[path_effects.SimpleLineShadow(),path_effects.Normal()])
plt.fill_between(time_model, lat_model, y2=0, color='mediumseagreen', alpha=0.9)
plt.grid(False)
plt.xlabel("Time", fontsize=20)
plt.ylabel("Latency (ms)", fontsize=20)

# %% Save and show figure
plt.savefig('net_speed_plot.png')
plt.show()
