import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import os

import plotly.express as px

#------------------------------------------Funciones--------------------------------------------------------------------------------------#
def getRsquared(y_1,y_2):
    correlation_matrix = np.corrcoef(y_1, y_2)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    print(r_squared)
    return int(r_squared*100)

def generarMetricas(df,value,gastos):
    print(df.shape)	
    precision = getRsquared(df[value].values,df['Real'].values)	
    bv = gastos*(100-precision)/100
    if precision >= 85:
      style_card = CARD_ACCEPTABLE_STYLE
    else:
      style_card = CARD_NOT_ACCEPTABLE_STYLE		 
    return html.P('La precisión para ' + value + ' es: ' + str(precision) + '%, con un BV de: ' +
			str(bv), style=style_card)

#------------------------------------------Lectura de Dataset ----------------------------------------------------------------------------#
csv_files_path = os.path.join('data/results_test.csv')
data_df = pd.read_csv(csv_files_path)
mincuota = int(data_df['Cuota C.U'].min())
maxcuota = int(data_df['Cuota C.U'].max()+100)
mintarget = 0
maxtarget = 86000
stepcuota = int((maxcuota - mincuota)/11)
quartil1 = mincuota + (stepcuota*2)
quartil2 = mincuota + (stepcuota*5)
quartil3 = mincuota + (stepcuota*8)

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

CARD_NOT_ACCEPTABLE_STYLE = {
    'textAlign': 'center',
    'color': '#d40404'
}

CARD_ACCEPTABLE_STYLE = {
    'textAlign': 'center',
    'color': '#2bba07'
}

controls1 = dbc.FormGroup(
    [
        html.P('Modelos de Regresión', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Modelo Regresión',
                'value': 'Modelo Regresion'
            }, {
                'label': 'Modelo Ridge',
                'value': 'Modelo Ridge'
            }, {
                'label': 'Modelo Lasso',
                'value': 'Modelo Lasso'
            }, {
		'label': 'Modelo Huber',
                'value': 'Modelo Huber'
	    }, {
		'label': 'Resultado Real',
                'value': 'Real'
	    }  
            ],
            value=['Modelo Regresion','Real'],  # default value
            multi=True
        ),
        html.Br(),
        html.P('Cantidad de Botellas', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=mincuota,
            max=maxcuota,
            step=stepcuota,
            value=[mincuota, maxcuota],
	    marks={
		mincuota: str(mincuota),
		quartil1: str(quartil1),
		quartil2: str(quartil2),
		quartil3: str(quartil3),
		maxcuota: str(maxcuota)						
		}
        ),
        html.Br(),
	html.P('Gastos logísticos', style={
            'textAlign': 'center'
        }),
	dbc.Input(id="input_gastos", placeholder="Gastos Logísticos", type="number", value=400000),
        html.Br(),	
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Actualizar',
            color='primary',
            block=True
        )        
    ]
)

controls2 = dbc.FormGroup(
    [
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
	html.Hr(),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value='value1',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        )
    ]
)

sidebar = html.Div(
    [
        html.H2('Parámetros', style=TEXT_STYLE),
        html.Hr(),
        controls1
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Resultados de Modelos Entrenados'], className='card-title',
                                style=CARD_TEXT_STYLE)
                        #,html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=9
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('Business Value', className='card-title', style=CARD_TEXT_STYLE)
                        #,html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    )
#    ,dbc.Col(
#        dbc.Card(
#            [
#                dbc.CardBody(
#                    [
#                        html.H4('Card Title 3', className='card-title', style=CARD_TEXT_STYLE),
#                        html.P('Sample text.', style=CARD_TEXT_STYLE),
#                    ]
#                ),
#            ]

#        ),
#        md=3
#    ),
#    dbc.Col(
#        dbc.Card(
#            [
#                dbc.CardBody(
#                    [
#                        html.H4('Card Title 4', className='card-title', style=CARD_TEXT_STYLE),
#                        html.P('Sample text.', style=CARD_TEXT_STYLE),
#                    ]
#                ),
#            ]
#        ),
#        md=3
#    )
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=9
        ),
        dbc.Col(
            dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(id='card_title_5', children=['Resultados de Modelos Entrenados'], className='card-title',
                                style=CARD_TEXT_STYLE)
                        #,html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
            ), md=3
        )
    ]
)

content = html.Div(
    [
        html.H2('Estimador de facturación mensual para bebidas gasificadas', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        #content_second_row,
        #content_third_row,
        content_fourth_row
    ],
    style=CONTENT_STYLE
)

#-------------------------------------------------Configuración de variables--------------------------------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
server = app.server
app.layout = html.Div([sidebar, content])



#@app.callback(
#    Output('graph_1', 'figure'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)
#    fig = {
#        'data': [{
#            'x': [1, 2, 3],
#            'y': [3, 4, 5]
#        }]
#    }
#    return fig


#@app.callback(
#    Output('graph_2', 'figure'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)
#    fig = {
#        'data': [{
#            'x': [1, 2, 3],
#            'y': [3, 4, 5],
#            'type': 'bar'
#        }]
#    }
#    return fig


#@app.callback(
#    Output('graph_3', 'figure'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)
#    df = px.data.iris()
#    fig = px.density_contour(df, x='sepal_width', y='sepal_length')
#    return fig


#@app.callback(
#    Output('graph_4', 'figure'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)  # Sample data and figure
#    df = px.data.gapminder().query('year==2007')
#    fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
#                         hover_name='country', size='pop', projection='natural earth')
#    fig.update_layout({
#        'height': 600
#    })
#    return fig


@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value')])
def update_graph_5(n_clicks, dropdown_value, range_slider_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    df = data_df[(data_df['Cuota C.U']>=range_slider_value[0]) & (data_df['Cuota C.U']<=range_slider_value[1])]
    fig = px.scatter(df, x='Cuota C.U', y=dropdown_value, range_x=[range_slider_value[0],range_slider_value[1]],
			range_y=[mintarget,maxtarget],labels={"Cuota C.U": "# Botellas"},)
    return fig


#@app.callback(
#    Output('graph_6', 'figure'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)  # Sample data and figure
#    df = px.data.tips()

#    fig = px.bar(df, x='total_bill', y='day', orientation='h')
#    return fig


@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value):
    return 'Resultados de Modelo de regresión'

@app.callback(
    Output('card_title_5', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('input_gastos', 'value')])
def update_card_title_5(n_clicks, dropdown_value, range_slider_value, gastos_value):
    print(dropdown_value)	
    df = data_df[(data_df['Cuota C.U']>=range_slider_value[0]) & (data_df['Cuota C.U']<=range_slider_value[1])]
    return [generarMetricas(df, i, gastos_value) for i in dropdown_value]


#@app.callback(
#    Output('card_text_1', 'children'),
#    [Input('submit_button', 'n_clicks')],
#    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     State('radio_items', 'value')
#     ])
#def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#    print(n_clicks)
#    print(dropdown_value)
#    print(range_slider_value)
#    print(check_list_value)
#    print(radio_items_value)  # Sample data and figure
#    return 'Card text change by call back'


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
