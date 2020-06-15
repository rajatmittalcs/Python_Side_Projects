# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:41:52 2020

@author: RAJAT
"""
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html


app=dash.Dash()

df=pd.read_csv('India_data.csv', sep='\t');
df.columns=['SN','State','Active','Cured','Deaths','Confirmed']
df=df.drop(columns=['SN','Cured'])

covX=df['State']
covY=df['Deaths']
covZ=df['Confirmed']
covA=df['Active']

data=[go.Scatter(x=covZ,y=covY,text=covX,mode='markers',
                 marker=dict(size=covA/500))]

layout=go.Layout(title='India Covid Analysis',
                 xaxis = dict(title = 'Confirmed Cases'),
                 yaxis = dict(title = 'Deaths'),
                 hovermode='closest')


app.layout=html.Div(dcc.Graph(id='main graph',figure=dict(data=data,layout=layout)))

if __name__=='__main__':
    app.run_server()