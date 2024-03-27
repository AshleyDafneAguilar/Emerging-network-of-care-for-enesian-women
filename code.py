#!/usr/bin/env python
# coding: utf-8
#Ashley Dafne Aguilar Salinas


"""## Librerías
"""
!pip install contextily
import pandas as pd
import geopandas as gpd
from pandas import ExcelFile

import openpyxl
import contextily

import numpy as np
import matplotlib.pyplot as plt

"""## Función
"""
#Permite agregar un mapa base de alta calidad 
#en el fondo de un gráfico de datos geoespaciales
#Esta función utiliza el servicio web de mapas base(OSM).
def on_basemap(ax):
    ax.set_aspect('equal')
    contextily.add_basemap(
      ax, 
      source=contextily.providers.OpenStreetMap.Mapnik
    )
    return ax
# ---

"""## Lectura del archivo .xlsx
"""

PATH = './dataset/'
xlsx = pd.ExcelFile(PATH + "Identificación de Problemáticas.xlsx", engine='openpyxl')
df = xlsx.parse(sheet_name='Casos')

#Mostramos el DataFrame
df

# ---
"""## Limpieza


###  Valores Nulos
"""

# Visualizamos los valores nulos
df.iloc[24:37]

#Borramos los valores nulos 
#de nuestro DataFrame
df.drop([x for x in range(24, 38, 1)], inplace=True)
df.reset_index(drop = True, inplace = True)

#Mostramos los cambios
df
# ---

"""## Caminos
"""
#Obtenemos todos los datos que
#son indicados como caminos 
df[df['Notas'].str.contains('Camino') == True]
# ---

"""## Puntos
"""
#Obtenemos todos los datos que
#no son indicados como caminos
#y los almacenamos como puntos
df_puntos = df.drop(df.index[df['Notas'].str.contains('Camino') == True])

#Mostramos los datos
#indicados como puntos
df_puntos
# ---

"""## Graficar
"""
#Convertimos el DataFrame de 
#los datos marcados como puntos 
#a un Geopandas.Se elimina el 
#último dato porque no hay información
geodf_puntos =  gpd.GeoDataFrame(df_puntos.drop([32]))
geodf_puntos.reset_index(drop = True, inplace = True)
geodf_puntos

#convertimos las columnas de Longitud y
#Latitud en un solo atributo de tipo POINT
gpd.GeoDataFrame(geometry=gpd.points_from_xy(geodf_puntos['Longitud'], geodf_puntos['Latitud']))

#Almacenamos ese cambio en un nuevo
#atributo denominado geometry
geodf_puntos['geometry'] = gpd.GeoDataFrame(geometry=gpd.points_from_xy(geodf_puntos['Latitud'], geodf_puntos['Longitud']))

#Mostramos los cambios 
#hechos al GeoDataFrame
geodf_puntos
# ---


"""## Coordenadas
"""

# Para obtener el CRS actual de un 
#GeoDataFrame, se puede utilizar la 
#función .crs sin argumentos.
geodf_puntos.crs

#Cambiar el sistema de referencia de 
#coordenadas(CRS) de un GeoDataFrame
#EPSG 4326 es empleado para la 
#representación de la cartografía a nivel mundial.
geodf_puntos = geodf_puntos.set_crs("EPSG:4326") 

#Transformamos las coordenadas a ESPDG 3857 
#que es el que utilizan la mayoría de los 
#mapas representados en la web
geodf_puntos = geodf_puntos.to_crs(epsg=3857)
# ---


#Ploteamos los puntos de nuestro 
#GepoDataFrame en el mapa
on_basemap(geodf_puntos.to_crs(epsg=3857).plot(figsize=(30,30)))
on_basemap(geodf_puntos.plot())


#Visualiza los puntos fuera del mapa
#geodf_puntos.explore(legend=False)
geodf_puntos['geometry'].plot()

# ---


