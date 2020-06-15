# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:49:20 2020

@author: RAJAT
"""

import pandas as pd
#import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table


app=dash.Dash()

df=pd.read_csv('state_wise_daily.csv')
df=df.rename(columns={'TT' : 'Total'})
df=df.drop(columns=['UN','TG','LD'])
lats=pd.read_csv('latlong.csv',sep='\t')

dftablecon=pd.DataFrame(df[df['Status']=='Confirmed'].sum(axis=0)).drop(['Date','Status']).rename(columns={0:'Confirmed'})
dftablerec=pd.DataFrame(df[df['Status']=='Recovered'].sum(axis=0)).drop(['Date','Status']).rename(columns={0:'Recovered'})
dftabledec=pd.DataFrame(df[df['Status']=='Deceased'].sum(axis=0)).drop(['Date','Status']).rename(columns={0:'Deceased'})
dftablecon.index=[i for i in range(36)]
dftablerec.index=[i for i in range(36)]
dftabledec.index=[i for i in range(36)]
dftable=pd.concat([lats.drop(columns=['Latitude','Longitude']),dftablecon,dftablerec,dftabledec],axis=1)

status=['Confirmed','Recovered','Deceased']

Condata=[sum(df[df['Status']=='Confirmed']['Total'][:i+1]) for i in range(len(df[df['Status']=='Confirmed']))]
Decdata=[sum(df[df['Status']=='Deceased']['Total'][:i+1]) for i in range(len(df[df['Status']=='Deceased']))]
Recdata=[sum(df[df['Status']=='Recovered']['Total'][:i+1]) for i in range(len(df[df['Status']=='Recovered']))]

app.layout=html.Div([
                     html.Div(f'{Condata[-1]}',style=dict(fontSize=30,color='orange',float='left',width='25%')),
                     html.Div(f'{Decdata[-1]}',style=dict(fontSize=30,color='red',float='left',width='25%')),
                     html.Div(f'{Recdata[-1]}',style=dict(fontSize=30,color='green',float='left',width='25%')),
                     html.Div(f'{round(Decdata[-1]/(Recdata[-1]+Decdata[-1]),4)}%',style=dict(fontSize=30,color='blue',float='left',width='25%')),
                     html.Div('Confirmed',style=dict(fontSize=15,color='orange',float='left',width='25%')),
                     html.Div('Deaths',style=dict(fontSize=15,color='red',float='left',width='25%')),
                     html.Div('Recovered',style=dict(fontSize=15,color='green',float='left',width='25%')),
                     html.Div('Death Rate',style=dict(fontSize=15,color='blue',float='left',width='25%')),
                     html.Div([dash_table.DataTable(id='covtable',
                                columns=[{"name": i, "id": i} for i in dftable.columns],
                                data=dftable.to_dict('records'),
                                sort_action='native',sort_mode='multi',
                                style_table=dict(maxHeight=520,overflowY='scroll'))],style=dict(width='35%',display= 'inline-block')),
                    html.Div([dcc.Graph(id='map'),
                     dcc.RadioItems(id='Status',
                                    options=[dict(label=status[i],value=i) for i in range(len(status))],
                                    value=0
                                    ),
                    dcc.Slider(id='timeslider',
                               min=3,
                               max=df.index.max(),
                               value=df.index.max(),
                               step=3,updatemode='drag'                               
                            ),'Use Slider to go backward/forward in time'],
                               style={'width':'60%', 'float':'right','textAlign': 'center','display': 'inline-block'}),
                               html.Div([html.Div([dcc.Graph(figure=dict(
                                       data=[go.Scatter(x=df[df['Status']=='Confirmed']['Date'],y=Condata,mode='lines')],
                                       layout=go.Layout(title='Confirmed Case Time Series',yaxis=dict(title='No. of Cases'))
                                       ))],style=dict(width='45%',display='inline-block',float='left')),
                                       html.Div([dcc.Graph(figure=dict(
                                       data=[go.Scatter(x=df[df['Status']=='Deceased']['Date'],y=Decdata,mode='lines')],
                                       layout=go.Layout(title='Deceased Case Time Series',yaxis=dict(title='No. of Cases'))
                                       ))],style=dict(width='45%',display='inline-block',float='right'))
                                       ])
                               ])

@app.callback(Output('map','figure'),
              [Input('timeslider','value'),
               Input('Status','value')]
        )

def update_time_data(tvalue,svalue):
    colors = ["orange","lightseagreen",'crimson']
    df2=df.iloc[:tvalue]
    i=svalue
    lon=lats['Longitude'].drop(0)
    lat=lats['Latitude'].drop(0)
    con=df2[df2['Status']=='Confirmed'].sum(axis=0)[3:]
    con=con.astype('int')+1
    rec=df2[df2['Status']=='Recovered'].sum(axis=0)[3:]
    rec=rec.astype('int')
    dec=df2[df2['Status']=='Deceased'].sum(axis=0)[3:]
    dec=dec.astype('int')
    stat=[f"{lats['States'][i+1]} Confirmed: {con[i]} Deceased: {dec[i]}" for i in range(len(con))]
    statuses=[con,rec,dec]
    fig=go.Figure()
    
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
            showlegend = True,legend=dict(itemsizing='constant',font=dict(size=15)),width=800,height=450
        )
    return fig
  
    
if __name__ == '__main__':
    app.run_server()