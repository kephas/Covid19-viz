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


#ConfirmedCases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
#Deaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
#Recoveries_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')


map = folium.Map(location=[0,0],
              tiles = 'Stamen Terrain',
              zoom_start=3)


points = (ConfirmedCases_raw.Lat,ConfirmedCases_raw.Long)
date_to_analyze='3/14/20'
radius = ConfirmedCases_raw[date_to_analyze].values.astype('float')

# Setting lat and long 
lat = points[0]
long = points[1]

for la,lo,ra in zip(lat[0:500],long[0:500],radius[0:500]):
    folium.Circle(
        location=[la,lo],
        radius=ra*10
    ).add_to(map)


map.save("./mymap.html")