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
from folium import IFrame
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
          self.aggregated.at['United Kingdom','Lat']=49.3723
          self.aggregated.at['United Kingdom','Long']=-2.3644
          self.aggregated.at['Denmark','Lat']=56.2639
          self.aggregated.at['Denmark','Long']=9.5018          



class CovidData(object):

    def __init__(self):
        self.confirmed_cases = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
        self.deaths = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
        self.recoveries = CovidDF('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
        self.loaded = False
        self.map = folium.Map(location=[10,20],
              tiles = 'Stamen Terrain',
              zoom_start=3)
        
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
          



my_date=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv').columns[-1]
covid_data=CovidData()
covid_data.populate(my_date)
covid_data.plot_number_of_cases_for_all_dataframes(my_date)

#iframe = folium.IFrame(str(my_date), width=700, height=450)
#popup = folium.Popup(str(my_date), max_width=3000)
#Text = folium.Marker(location=[70,0], popup=popup,
#                     icon=folium.Icon(icon_color='green'))
#covid_data.map.add_child(Text)

legend_html =   '''
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; width: 300px; height: 100px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            ">&nbsp; Occurences of covid-19 cases by country <br>
                              &nbsp; Confirmed cases &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
                              &nbsp; Deaths &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
                              &nbsp; Recoveries &nbsp; <i class="fa fa-circle" style="color:green"></i>
                </div>
                '''
                
covid_data.map.get_root().html.add_child(folium.Element(legend_html))


covid_data.map.save("./mytest.html")
#
#app = Flask(__name__)
#@app.route("/")
#def display_map():
#     return covid_data.map._repr_html_()
#
#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
