# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 01:14:15 2020

@author: RAJAT
"""

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import folium
import plotly.express as px


app=dash.Dash()

df=pd.read_csv('state_wise_daily.csv')
df=df.rename(columns={'TT' : 'Total'})
df=df.drop(columns=['UN','TG','LD'])

lats=pd.read_csv('latlong.csv',sep='\t')

latestdata=df.iloc[-3:].drop(columns=['Date','Total']).T
header=latestdata.iloc[0]
latestdata=latestdata[1:]
latestdata.columns=header
indices=pd.DataFrame(latestdata.index)
latestdata.index=[i for i in range(35)]

conf=pd.DataFrame(latestdata['Confirmed'])
normCon=conf/conf.std()
normCon.columns=['NormConf']

combinedData=pd.concat([latestdata,lats,indices,normCon],axis=1)

combinedData=combinedData.rename(columns={0:'Statecode'})


lat=combinedData['Latitude']
lon=combinedData['Longitude']
stat=combinedData['States']
con=combinedData['Confirmed']
dec=combinedData['Deceased']


map=folium.Map(zoom_start=50)

for i in range(len(combinedData['Statecode'])):
    
    folium.CircleMarker(location =[lat.iloc[i],
                                   lon.iloc[i]],
    radius = combinedData['NormConf'].iloc[i]*15,
    tooltip=f"{stat.iloc[i]} \n Confirmed : {con.iloc[i]} \n Deceased : {dec.iloc[i]}",
    popup=f"{stat.iloc[i]} \n Confirmed : {con.iloc[i]} \n Deceased : {dec.iloc[i]}").add_to(map)
map.save('temp.html')


app.layout=html.Div([
        html.Iframe(id='map',srcDoc=open('temp.html','r').read(),width='90%',height='600px'),
        ],
        style=dict(border='5 px red solid')
        )


if __name__ == '__main__':
    app.run_server()