#!/usr/bin/env python
# coding: utf-8
#Ashley Dafne Aguilar Salinas


"""# Librerías
"""

import pandas as pd
import geopandas as gpd

import openpyxl
import contextily

from pandas import ExcelFile

import numpy as np
import matplotlib.pyplot as plt


# # Función

# In[2]:


def on_basemap(ax):
    ax.set_aspect('equal')
    contextily.add_basemap(
      ax, 
      source=contextily.providers.OpenStreetMap.Mapnik
    )
    return ax


# # Lectura del DataFrame

# In[3]:


PATH = './data/'


# In[4]:


xlsx = pd.ExcelFile(PATH + "Identificación de Problemáticas.xlsx", engine='openpyxl')


# In[5]:


df = xlsx.parse(sheet_name='Casos')


# In[6]:


df


# ---

# # Limpieza

#  Nulos

# In[7]:


df.iloc[24:37]


# In[8]:


df.drop([x for x in range(24, 38, 1)], inplace=True)


# In[9]:


df.reset_index(drop = True, inplace = True)


# In[10]:


df


# ---

# # Caminos

# In[11]:


df[df['Notas'].str.contains('Camino') == True]


# ---

# # Puntos

# In[12]:


df_puntos = df.drop(df.index[df['Notas'].str.contains('Camino') == True])


# In[13]:


df_puntos


# ---

# # Graficar

# In[14]:


#se elimina el último dato porque no hay información

geodf_puntos =  gpd.GeoDataFrame(df_puntos.drop([32]))


# In[15]:


geodf_puntos.reset_index(drop = True, inplace = True)
geodf_puntos


# In[16]:


gpd.GeoDataFrame(geometry=gpd.points_from_xy(geodf_puntos['Longitud'], geodf_puntos['Latitud']))


# In[17]:


geodf_puntos['geometry'] = gpd.GeoDataFrame(geometry=gpd.points_from_xy(geodf_puntos['Latitud'], geodf_puntos['Longitud']))


# In[18]:


geodf_puntos


# ## Coordenadas

# In[19]:


geodf_puntos.crs


# In[20]:


geodf_puntos = geodf_puntos.set_crs("EPSG:4326") 


# In[21]:


geodf_puntos = geodf_puntos.to_crs(epsg=3857)


# In[22]:


on_basemap(geodf_puntos.to_crs(epsg=3857).plot(figsize=(30,30)))


# In[23]:


on_basemap(geodf_puntos.plot())


# In[24]:


#geodf_puntos.explore(legend=False)


# In[25]:


geodf_puntos['geometry'].plot()


# ---

# ---

# ## AGEBS

# In[7]:


PATh = './mapping/'
agebs = gpd.read_file(PATh + 'conjunto de datos/16a.shp')


# In[8]:


agebs


# In[58]:


# Morelia
agebs_Morelia = agebs[agebs['CVE_MUN'] == '053'].reset_index(drop=True)
agebs_Morelia


# In[59]:


agebs_Morelia = agebs_Morelia.to_crs(epsg=6369)


# In[60]:


agebs_Morelia.plot()
plt.title('Zonas AGEB en Morelia')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.show()


# In[62]:


# La proyección que utilizamos no es compatible aún con contextily entonces usamos otra temporalmente
# Sólo para hacer la visualización en el mapa
on_basemap(agebs_Morelia.to_crs(epsg=3857).plot(figsize=(50,50),alpha=0.5))
plt.title('Mapa de Morelia con AGEBs')
plt.show()


# In[67]:


on_basemap(geodf_puntos['geometry'].plot())


# In[ ]:




