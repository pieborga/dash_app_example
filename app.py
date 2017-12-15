
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# 
# The dashboard will have two graphs: 
# 
# The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators.
# 

# In[2]:

import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[5]:

#Import files & create coresponding indicators for values and countries

euro_data = pd.read_csv('/Users/Pietro/Documents/GitHub/dash_app_example/Eurostat_file.csv')

available_indicators = euro_data['NA_ITEM'].unique()

available_countries = euro_data['GEO'].unique()


# ### My Dashboard

# In[ ]:

#Create app itself

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Create dataframe for units that will be used

euro_data1 = euro_data[euro_data['UNIT'] == 'Current prices, million euro']

#Start designing the layout of app

app.layout = html.Div([

#Part will be for graph 1    

    html.Div([
#Create the layout of first dropdown and set default value for graph - Gross domestic product market prices
        html.Div([
            dcc.Dropdown( 
#Given a unique axis name here xaxis1 
#Ddropdown will affect both graphs, same  done for the yaxis
                id='xaxis1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),
#Same steps as for the x axis,default value to Wages and Salaries
        html.Div([
            dcc.Dropdown( 
                id='yaxis1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),

#Give graph a unique name grph1 in order to be able to have both graphs on my dashboard
    dcc.Graph(id='grph1'),
#Create slider, in order to manipulate position made it as a html and with style aligned it with the graph itself
    html.Div(dcc.Slider( 
        id='year--slider',
        min=euro_data['TIME'].min(),
        max=euro_data['TIME'].max(),
        value=euro_data['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in euro_data['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

#Create the environment for second chart following the same steps as before
    
    html.Div([
        
        html.Div([
            dcc.Dropdown( 
#Use xaxis2 as my id to prevent the dropdown from previous graph to interact with this axis and vice-versa
                id='xaxis2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
# Use available_countries as the option for dropdown and set Spain as the default value
        html.Div([
            dcc.Dropdown( 
                id='yaxis2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
# Give second graph a unique id graph2
     dcc.Graph(id='grph2'),


])

#HCreate the callback which updates the first graph according to the value in the dropdown boxes
#Start by setting imputs and outputs
@app.callback(
    dash.dependencies.Output('grph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

#Define the function
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

#Create dataframe which will match the coresponding value with the year that is chosen
    euro_data_yearly = euro_data[euro_data['TIME'] == year_value]
#Finally create the output, in addition to the values on the x and y axis, add text marker which shows the country,
#when you hover over the coresponding scatter value with the cursor
    return {
        'data': [go.Scatter(
            x=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            text=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
# Set margins for both of the charts to be the same for a neater look of dashboard
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#Create the call back for the second chart, starting with defining the input and output using the id's assigned
#to second graph and coresponding ones for the x and y axis
@app.callback(
    dash.dependencies.Output('grph2', 'figure'),
    [dash.dependencies.Input('xaxis2', 'value'),
     dash.dependencies.Input('yaxis2', 'value')])
#Update the column names of the chart
def update_graph(xaxis_column_name, yaxis_column_name):
#Create a dataframe which will mach the country or country group with the coresponding x axis value    
    euro_data_yearly = euro_data1[euro_data1['GEO'] == yaxis_column_name]

#Create output, using mode='lines' to create a linechart. Note that here no need for text= as there is nothing to
#label on the chart area itself, as it will show values for only the country chosen in the dropdown
    return {
        'data': [go.Scatter(
            x=euro_data_yearly['TIME'].unique(),
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#Run the server for my dashboard

if __name__ == '__main__':
    app.run_server()


# In[ ]:



