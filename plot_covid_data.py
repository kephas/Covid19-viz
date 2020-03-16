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
import flask
from flask import Flask




class CovidDF:
    def __init__(self, url):
        self.url = url
        self.raw = None
        self.aggregated = None

    def reload(self, date):
        self.raw = pd.read_csv(self.url)
        self.group_by_regions(date)

    def group_by_regions(self,date):
          df=self.raw[['Province/State','Country/Region','Lat','Long',date]]
          self.aggregated=df.groupby(['Country/Region']).agg({'Lat':'mean',
                              'Long':'mean',
                              date: 'sum'})
          self.aggregated.at['France','Lat']=46.2276
          self.aggregated.at['France','Long']=2.2137


class CovidData(object):

    def __init__(self):
        self.confirmed_cases = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
        self.deaths = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
        self.recoveries = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
        self.loaded = False
        self.map = folium.Map(location=[0,0],
              tiles = 'Stamen Terrain',
              zoom_start=2)
        
    def populate(self, date):
        if not self.loaded:
             self.confirmed_cases.reload(date)
             self.deaths.reload(date)
             self.recoveries.reload(date)
             self.loaded=True

    def plot_number_of_cases(self,df,date,custom_color):
          dc=df.iloc[df[date].to_numpy().nonzero()]
          latitude = dc.Lat.values.astype('float')
          longitude = dc.Long.values.astype('float')
          radius = dc[date].values.astype('float')
     
          for la,lo,ra in zip(latitude,longitude,radius):
              folium.Circle(
                  location=[la,lo],
                  radius=ra*10,
                  fill=True,
                  color=custom_color,
                  fill_color=custom_color,
                  fill_opacity=0.5
              ).add_to(self.map)

    def plot_number_of_cases_for_all_dataframes(self,date):
          self.plot_number_of_cases(self.confirmed_cases.aggregated,date,'blue')
          self.plot_number_of_cases(self.deaths.aggregated,date,'red')
          self.plot_number_of_cases(self.recoveries.aggregated,date,'green')
          



my_date='3/14/20'
covid_data=CovidData()
covid_data.populate(my_date)
covid_data.plot_number_of_cases_for_all_dataframes(my_date)
#covid_data.map.save("./mytest.html")

app = Flask(__name__)
@app.route("/")
def display_map():
     return covid_data.map._repr_html_()




