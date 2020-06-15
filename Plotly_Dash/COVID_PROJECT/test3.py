# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:17:10 2020

@author: RAJAT
"""


import pandas as pd
#import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app=dash.Dash()

df=pd.read_csv('state_wise_daily.csv')
df=df.rename(columns={'TT' : 'Total'})
df=df.drop(columns=['UN','TG','LD'])
lats=pd.read_csv('latlong.csv',sep='\t')

app.layout=html.Div([dcc.Graph(id='map'),
                    dcc.Slider(id='timeslider',
                               min=3,
                               max=df.index.max(),
                               value=df.index.max(),
                               step=3,updatemode='drag'                               
                            ),html.Div(['Use Slider to go backward/forward in time'])])

@app.callback(Output('map','figure'),
              [Input('timeslider','value')]
        )

def update_time_data(tvalue):
    colors = ["orange","lightseagreen",'crimson']
    status=['Confirmed','Recovered','Deceased']
    df2=df.iloc[:tvalue]
    lon=lats['Longitude']
    lat=lats['Latitude']
    con=df2[df2['Status']=='Confirmed'].sum(axis=0)[3:]
    con=con.astype('int')+1
    rec=df2[df2['Status']=='Recovered'].sum(axis=0)[3:]
    rec=rec.astype('int')
    dec=df2[df2['Status']=='Deceased'].sum(axis=0)[3:]
    dec=dec.astype('int')
    stat=[f"{lats['States'][i]} Confirmed: {con[i]} Deceased: {dec[i]}" for i in range(len(con))]
    statuses=[con,rec,dec]
    fig=go.Figure()
    
    for i in range(3):
        fig = fig.add_trace(go.Scattergeo(
                lon = lon,
                lat = lat,
                text = stat,
                mode = 'markers',
                marker=dict(size=statuses[i]/statuses[i].std()*10,
                color=colors[i],sizemode='diameter')
                ,name=status[i]
                ))

        fig.update_layout(
            title = 'India CoViD 2019',
            geo_scope='asia',
            showlegend = True,legend=dict(itemsizing='constant',font=dict(size=15)),width=1368,height=500
        )
    return fig

if __name__ == '__main__':
    app.run_server()