#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:01:50 2020

@author: sheldon
"""

import os 
import pandas as pd
import path
import folium
from folium import plugins
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et
import pdb 
import flask
from flask import Flask



############# LOAD DATAFRAMES

class CovidData(object):

    def __init__(self):
        self.confirmed_cases_raw = None
        self.deaths_raw = None
        self.recoveries_raw = None
        self.confirmed_cases_aggregated = None
        self.deaths_aggregated = None
        self.recoveries_aggregated = None
        self.loaded = False
        self.map = folium.Map(location=[0,0],
              tiles = 'Stamen Terrain',
              zoom_start=3)
        
    def populate(self):
        if not self.loaded:
             self.confirmed_cases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
             self.deaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
             self.recoveries_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
             self.loaded=True

        
     
    def group_by_regions(self,df,date):
          df=df[['Province/State','Country/Region','Lat','Long',date]]
          df_aggregated=df.groupby(['Country/Region']).agg({'Lat':'mean', 
                              'Long':'mean', 
                              date: 'sum'})
          df_aggregated.set_value('France','Lat',46.2276)
          df_aggregated.set_value('France','Long',2.2137)
          return df_aggregated

    def group_by_regions_for_all_dataframes(self,date):
          self.confirmed_cases_aggregated=self.group_by_regions(self.confirmed_cases_raw,date)
          self.deaths_aggregated=self.group_by_regions(self.deaths_raw,date)
          self.recoveries_aggregated=self.group_by_regions(self.recoveries_raw,date)

    def plot_number_of_cases(self,df,date,custom_color):
          dc=df.iloc[df[date].nonzero()]
          latitude = dc.Lat.values.astype('float')
          longitude = dc.Long.values.astype('float')
          radius = dc[date].values.astype('float')
     
          for la,lo,ra in zip(latitude,longitude,radius):
              folium.Circle(
                  location=[la,lo],
                  radius=ra*10,
                  fill=True,
                  color=custom_color,
                  fillColor=custom_color,
                  fillOpacity=0.5
              ).add_to(self.map)

    def plot_number_of_cases_for_all_dataframes(self,date):
          self.plot_number_of_cases(self.confirmed_cases_aggregated,date,'blue')
          self.plot_number_of_cases(self.deaths_aggregated,date,'red')
          self.plot_number_of_cases(self.recoveries_aggregated,date,'green')
   

my_date='3/14/20'
covid_data=CovidData()
covid_data.populate()
covid_data.group_by_regions_for_all_dataframes(my_date)
covid_data.plot_number_of_cases_for_all_dataframes(my_date)
       
app = Flask(__name__)
@app.route("/")
def display_map():
     return covid_data.map.render()




