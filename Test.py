# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:02:54 2024

@author: harry
"""
# Import packages
import matplotlib.pyplot as plt
import pandas as pd
import cartopy
import datetime
from datetime import datetime

#%% Read in appropriate files and datasets. Change for locally saved files.

# Read in files
file = open("Test.csv")
gps_file = open("gps.csv")

# Open files as datasets
dataset = pd.read_csv(file)
gps_data = pd.read_csv(gps_file)

#%% Data conversions to amend for having multiple csv files.

# Need to convert datetime columns to datetime objects:
# Converts in format dd/mm/yyyy hh:mm:ss
dataset["date"] = pd.to_datetime(dataset['date'], format='%d/%m/%Y %H:%M:%S')
gps_data["gps_datetime"] = pd.to_datetime(gps_data['gps_datetime'], format='%d/%m/%Y %H:%M:%S')

# sort to ensure chronology
dataset_sorted = dataset.sort_values('date')
gps_data_sorted = gps_data.sort_values('gps_datetime')

# Merge through by matching nearest datetime values
data = pd.merge_asof(dataset_sorted, gps_data_sorted, left_on='date', right_on='gps_datetime', direction='nearest')

# We can extract time from our datetime data if we are interested in daily cycles
data['time'] = data['date'].dt.time
# We also need to convert this into plottable data
data['time_numeric'] = data['time'].apply(lambda x: x.hour + x.minute / 60 + x.second / 3600)

# %% Doing the same by date allows us to compute daily means etc.

# Do the same for date:
data['day'] = data['date'].dt.date

# We can now calculate the mean temperature, etc. of our data by grouping by the day it was measured on:
day_temp = data.groupby('day')['temperature'].mean()
# This returns a series with the index being the day and the values are the temperatures
day_humid = data.groupby('day')['humidity'].mean()
day_pressure = data.groupby('day')['pressure'].mean()
#%% Do some plotting

# This figure plots a timeseries of temperature
# Start figure
plt.figure(figsize=(10,6))
# Tell it what to plot
plt.plot(data['date'], data['temperature'])
# Label axes
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
# to save the figure, delete the hashtag, re-run and change name from timeseries.png
# plt.savefig('timeseries.png', dpi = 300)
plt.show()

# This figure plots a timeseries of temperature but with the day component removed
# Start figure
plt.figure(figsize=(10,6))
# scatter maybe more appropriate than line
plt.scatter(data['time_numeric'], data['temperature'])
# Label axes
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
# to save the figure, delete the hashtag, re-run and change name from timeseries.png
# plt.savefig('timeseries.png', dpi = 300)
plt.show()

# This figure plots a timeseries of temperature but as a daily mean
# Start figure
plt.figure(figsize=(10,6))
# tell it what to plot
plt.plot(day_temp.index, day_temp)
# label axes
plt.xlabel('Day')
plt.ylabel('Temperature (°C)')
# to save the figure, delete the hashtag, re-run and change name from timeseries.png
# plt.savefig('timeseries.png', dpi = 300)
plt.show()

# This figure maps temperature data on a scatterplot for our fieldwork
# Start figure
plt.figure(figsize=(10, 6))
# Setup axes with map projection
ax = plt.axes(projection = cartopy.crs.Robinson())
# Add coastlines
ax.coastlines(resolution = '10m')
# Add scattered data
sc = ax.scatter(data['longitude'], data['latitude'], c= data['temperature'], cmap = 'coolwarm', marker = 'o', transform = cartopy.crs.PlateCarree())
# Setup colorbar
cbar = plt.colorbar(sc, ax = ax, label = 'Temperature')
# Figure outline
ax.spines['geo'].set_linewidth(1)
# Setup gridlines
gl = ax.gridlines(linewidth=0.5, draw_labels=True, crs=cartopy.crs.PlateCarree())
# Remove right side and top of figure labels
gl.right_labels = False
gl.top_labels = False
# to save the figure, delete the hashtag and re-run
# plt.savefig('map.png', dpi = 300)
plt.show()


