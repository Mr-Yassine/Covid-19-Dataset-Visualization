#!/usr/bin/env python
# coding: utf-8

# # Covid-19 Data Analysis Visualization

# #### Packages installation

# In[1]:


get_ipython().system('pip install folium')
get_ipython().system('pip install plotly')


# ## Importing packages

# In[2]:


#imports

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly as py
py.offline.init_notebook_mode(connected = True)

import folium

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

import math
import random
from datetime import timedelta

import warnings
warnings.filterwarnings('ignore')

#color palette
cnf = '#393e46'
dth = '#ff2e63'
rec = '#21bf73'
act = '#fe9801'


# ## Data preparation

# In[3]:


#Importing the dataset (covid_19_data_cleaned.csv) with read_csv and (Reading date columns from a CSV file, By default, date columns are represented as object when loading data from a CSV file. so we use the parse_dates to read the date column correctly,)
df = pd.read_csv('Covid-19-Preprocessed-Dataset-master/preprocessed/covid_19_data_cleaned.csv', parse_dates = ['Date'])


# In[4]:


#Replace NAN values of the columns (province/state) with ''.
df['Province/State'] = df['Province/State'].fillna("")

#show the result
df


# ## Data info 

# In[5]:


print(df)


# In[6]:


df.shape


# In[7]:


df.columns


# In[8]:


#I'll call the value_counts() method on the country field to see the count of unique values for each country.
df['Country'].value_counts()


# ## Confirmed, Recovered, and Deaths Cases

# In[9]:


confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
recovered = df.groupby('Date').sum()['Recovered'].reset_index()
deaths = df.groupby('Date').sum()['Deaths'].reset_index()

cases = df.groupby('Date')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()

cases.tail()


# In[10]:


#count the number of missing values in Pandas dataframe
df.isnull().sum()


# In[11]:


#information about our data

df.info()


# In[12]:


#result of Morocco only
df.query('Country == "Morocco"')


# ## Worldwide Total Confirmed, Recovered, and Deaths

# In[13]:


confirmed.tail()


# In[14]:


recovered.tail()


# In[15]:


deaths.tail()


# In[16]:


#calling the figure function
fig = go.Figure()

#add the trace
fig.add_trace(go.Scatter (x = confirmed['Date'], y = confirmed['Confirmed'], name = 'confirmed', line = dict(color = "blue", width = 3)))
fig.add_trace(go.Scatter (x = recovered['Date'], y = recovered['Recovered'], name = 'Recovered', line = dict(color = "Orange", width = 3)))
fig.add_trace(go.Scatter (x = deaths['Date'], y = deaths['Deaths'], name = 'Deaths', line = dict(color = "Red", width = 3)))

#add a title to the figure and X, y axis
fig.update_layout(title = 'Worldwide Covid-19 Cases', xaxis_tickfont_size = 14, yaxis = dict (title = 'Number of Cases'))


#show the simple plot of the cases
fig.show()


# ## Cases Density Animation on World Map

# In[17]:


df.info()


# In[18]:


df['Date'] = df['Date'].astype(str)


# In[19]:


df.info()


# In[20]:


df.head()


# In[21]:


fig = px.density_mapbox (df, lat = 'Lat', lon = 'Long', hover_name = 'Country', hover_data = ['Confirmed', 'Recovered', 'Deaths'], animation_frame = 'Date', color_continuous_scale = 'Portland', radius = 7, zoom = 0, height = 700 )
fig.update_layout (title = 'Worldwide Covid-19 Cases with Time Laps')
fig.update_layout (mapbox_style = 'open-street-map', mapbox_center_lon = 0)

fig.show()


# ## Total Cases on Ships

# In[22]:


df['Date'] = pd.to_datetime(df['Date'])
df.info()


# In[23]:


# Ships
# =======================================

ship_rows = df['Province/State'].str.contains ('Morocco') | df ['Province/State'].str.contains ('Diamond Princess')
# df[ship_rows]

ship = df[ship_rows]
df = df[~ship_rows]


# In[24]:


ship_latest = ship[ship['Date'] == max (ship['Date'])]
ship_latest


# ## Cases Over the Time with Area Plot

# In[25]:


temp = df.groupby('Date')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
temp = temp[temp['Date'] == max(temp['Date'])].reset_index(drop = True)
# temp.tail()

tm = temp.melt(id_vars = 'Date', value_vars = ['Active','Deaths', 'Recovered'])
fig = px.treemap(tm, path = ['variable'], values = 'value', height = 250, width = 800, color_discrete_sequence = [act, rec, dth])

fig.data[0].textinfo = 'label+text+value'
fig.show()


# In[26]:


temp = df.groupby ('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
temp = temp.melt(id_vars = 'Date', value_vars = ['Recovered', 'Deaths', 'Active'], var_name = 'Case', value_name = 'Count')
temp

fig = px.area(temp, x = 'Date', y = 'Count', color = 'Case', height = 500, title = 'Cases over time', color_discrete_sequence= [rec, dth, act] )
fig.update_layout (xaxis_rangeslider_visible = True)
fig.show()


# # Folium Maps

# ### WorldWide Cases on Folium Maps

# In[27]:


temp = df[df['Date'] == max(df['Date'])]

m = folium.Map(location = [0,0], tiles ='cartodbpositron', min_zoom = 1, max_zoom = 4, zoom_start = 1)

for i in range (0, len(temp)):
    folium.Circle(location = [temp.iloc[i]['Lat'], temp.iloc[i]['Long']], color = 'crimson', fill = 'crimson', 
                  tooltip = '<li><bold> Country: ' + str(temp.iloc[i]['Country'])+
                            '<li><bold> Province: ' + str(temp.iloc[i]['Province/State'])+
                            '<li><bold> Confirmed: ' + str(temp.iloc[i]['Confirmed'])+
                            '<li><bold> Deaths: ' + str(temp.iloc[i]['Deaths']),
                  radius = int(temp.iloc[i]['Confirmed'])**0.6).add_to(m)
m


# ## Deaths and Recoveries per 100 Cases

# In[28]:


#Importing the dataset ('country_daywise.csv') with read_csv
country_daywise = pd.read_csv('Covid-19-Preprocessed-Dataset-master/preprocessed/country_daywise.csv', parse_dates = ['Date'])


# In[29]:


#show the dataset

country_daywise.head()


# In[30]:


#Importing the dataset ('countrywise.csv') with read_csv
countrywise = pd.read_csv('Covid-19-Preprocessed-Dataset-master/preprocessed/countrywise.csv')


# In[31]:


#show the dataset
countrywise.head()


# In[32]:


#Importing the dataset ('daywise.csv') with read_csv
daywise = pd.read_csv('Covid-19-Preprocessed-Dataset-master/preprocessed/daywise.csv', parse_dates = ['Date'])


# In[33]:


#show the dataset
daywise.head()


# In[34]:


fig_c = px.bar(daywise, x = 'Date', y = 'Confirmed', color_discrete_sequence = [act])

fig_d = px.bar(daywise, x = 'Date', y = 'Deaths', color_discrete_sequence = [dth])

fig = make_subplots(rows = 1, cols = 2, shared_xaxes = False, horizontal_spacing = 0.1,
                    subplot_titles=('Confirmed Cases', 'Deaths Cases'))

fig.add_trace(fig_c['data'][0], row = 1, col = 1)
fig.add_trace(fig_c['data'][0], row = 1, col = 2)

fig.update_layout(height = 400)

fig.show()


# ## Top 15 Countries Cases Analysis

# In[35]:


#Importing the dataset ('countrywise.csv') with read_csv
countywise = pd.read_csv('Covid-19-Preprocessed-Dataset-master/preprocessed/countrywise.csv')

countywise.columns


# In[36]:


top = 15

fig_c = px.bar(countywise.sort_values('Confirmed').tail(top), x = 'Confirmed', y = 'Country',
              text = 'Confirmed', orientation='h', color_discrete_sequence=[cnf])

fig_d = px.bar(countywise.sort_values('Deaths').tail(top), x = 'Deaths', y = 'Country',
              text = 'Deaths', orientation='h', color_discrete_sequence=[dth])

fig_a = px.bar(countywise.sort_values('Active').tail(top), x = 'Active', y = 'Country',
              text = 'Confirmed', orientation='h', color_discrete_sequence=[act])

fig_r = px.bar(countywise.sort_values('Recovered').tail(top), x = 'Recovered', y = 'Country',
              text = 'Deaths', orientation='h', color_discrete_sequence=[rec])


#result per 100 cases
fig_dc = px.bar(countywise.sort_values('Deaths / 100 Cases').tail(top), x = 'Deaths / 100 Cases', y = 'Country',
              text = 'Deaths / 100 Cases', orientation='h', color_discrete_sequence=['#FF0000'])

fig_rc = px.bar(countywise.sort_values('Recovered / 100 Cases').tail(top), x = 'Recovered / 100 Cases', y = 'Country',
              text = 'Recovered / 100 Cases', orientation='h', color_discrete_sequence=['#ADD8E6'])








fig = make_subplots(rows = 5, cols = 2, shared_xaxes=False, horizontal_spacing=0.2,
                   vertical_spacing=.05,
                   subplot_titles=('Confirmed Cases', 'Deaths Reported', 'Recovered Cases', 'Active Cases', 'Deaths / 100 Cases', 'Recovered / 100 Cases'))

fig.add_trace(fig_c['data'][0], row = 1, col = 1)
fig.add_trace(fig_d['data'][0], row = 1, col = 2)
fig.add_trace(fig_r['data'][0], row = 2, col = 1)
fig.add_trace(fig_a['data'][0], row = 2, col = 2)

fig.add_trace(fig_dc['data'][0], row = 3, col = 1)
fig.add_trace(fig_rc['data'][0], row = 3, col = 2)

fig.update_layout(height = 3000)

fig.show()


# # END
