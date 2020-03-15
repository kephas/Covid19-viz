#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:01:50 2020

@author: sheldon
"""

import os 
import folium
from folium import plugins
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et

m = folium.Map(location=[40.0150, -105.2705],
              tiles = 'Stamen Terrain')


m.save("./mymap.html")