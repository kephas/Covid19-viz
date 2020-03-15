#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:01:50 2020

@author: sheldon
"""

import os 
import pandas as pd
import folium
from folium import plugins
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et
import pdb 

############# LOAD DATAFRAMES
#ConfirmedCases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
#Deaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
#Recoveries_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')


def plot_number_of_cases(df,date,custom_color):
     
#     date_to_analyze='3/14/20'
     dc=df.iloc[df[date_to_analyze].nonzero()]

     latitude = dc.Lat.values.astype('float')
     longitude = dc.Long.values.astype('float')
     radius = dc[date_to_analyze].values.astype('float')



     for la,lo,ra in zip(latitude,longitude,radius):
         folium.Circle(
             location=[la,lo],
             radius=ra*10,
             fill=True,
             color=custom_color,
             fillColor=custom_color,
             fillOpacity=0.5
         ).add_to(map)

map = folium.Map(location=[0,0],
              tiles = 'Stamen Terrain',
              zoom_start=3)

plot_number_of_cases(ConfirmedCases_raw,'3/14/20','blue')
plot_number_of_cases(Deaths_raw,'3/14/20','red')


map.save("./mymap.html")