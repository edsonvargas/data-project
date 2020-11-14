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

def generarFacturacion(df_params,cuota,ingreso,check_list):
    print(df_params['Ing. Bruto  Cuota S/. Mensual'].values[0]) 	
    result = cuota * df_params['Cuota C.U'].values[0] +  ingreso * df_params['Ing. Bruto  Cuota S/. Mensual'].values[0]	
    result2 = ingreso * df_params['Ing. Neto  Cuota S/.  Mensual'].values[0] + df_params['intercepto'].values[0] 
    return (result+result2)


#------------------------------------------Lectura de Datasets ----------------------------------------------------------------------------#
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

csv_parametros_path = os.path.join('data/resultados_algoritmos_regresion.csv')
parametros_df = pd.read_csv(csv_parametros_path)

LOGO_PUCP = {
    'background': "url(''https://www.pucp.edu.pe/wp-content/themes/home-theme/images/logo-pucp.svg'')",
    'center': 'no-repeat'
}

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
#    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '100%',
    'padding': '15px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '0%',
    'margin-right': '0%',
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
        html.P('Modelos de Regresión', style=CARD_TEXT_STYLE),
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
        html.P('Cantidad de Botellas', style=CARD_TEXT_STYLE),
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
	html.P('Gastos logísticos', style=CARD_TEXT_STYLE),
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
        html.Br(),
	dcc.Dropdown(
            id='dropdown_test',
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
	    }
            ],
            value='Modelo Huber'
        ),
        html.Br(),	
	dbc.Row([
	  dbc.Col(html.P('Número de botellas', style=CARD_TEXT_STYLE),md=6),
	  dbc.Col(dbc.Input(id="input_cuota", placeholder="Ingrese cantidad", type="number", value=15),md=6)]),
        html.Br(),
	dbc.Row([
	  dbc.Col(html.P('Ingreso Bruto Mensual', style=CARD_TEXT_STYLE),md=6),
	  dbc.Col(dbc.Input(id="input_ingreso", placeholder="Ingrese cantidad", type="number", value=144),md=6)]),
        html.Br(),
        html.P('Marque si corresponde', style=CARD_TEXT_STYLE),
        html.Div(dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Locales tradicionales',
                'value': 'Canal ISSCOM_2_VIV.LOCALES TRADICIONALES'
            	},
                {
                    'label': 'Subregion ICA',
                    'value': 'Locacion Comercial_2_I3 ECOBESA ICA'
                },
		{
		    'label': 'Subregion Iquitos',
		    'value': 'Locacion Comercial_2_JC O.L. IQUITOS'		
		}
            ],
            inline=True
        ),style=TEXT_STYLE),
        html.Br(),
	dbc.Button(
            id='predecir_button',
            n_clicks=0,
            children='Calcular',
            color='primary',
            block=True
        )
])


parametros_card=dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Parámetros', className='card-title', style=CARD_TEXT_STYLE)
                    ]
                )
            ])


sidebar = html.Div(
    [
	parametros_card,
        html.Hr(),
        controls1
    ],
    style=SIDEBAR_STYLE,
)

sidebar_pred = html.Div(
    [
	parametros_card,
        controls2
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

content_first_pred_row = dbc.Row(
    [
        dbc.Col([	
	    dbc.Card(
            [
                dbc.CardBody(
                    [
		        html.Div(id='card_title_6', children=['Resultados del Modelo'], className='card-title',
                                style=CARD_TEXT_STYLE)
                    ]
                )
            ]
            )]
        )
    ]
)

content_second_pred_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=9
        ),
        dbc.Col([
	    html.Hr(),		
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
            )], md=3
        )
    ]
)

content = html.Div(
    [
        content_first_row,
        content_second_row
    ],
    style=CONTENT_STYLE
)

content_pred = html.Div(
    [
        content_first_pred_row
    ],
    style=CONTENT_STYLE
)

tab1_content = html.Div(
		[
		dbc.Col(sidebar, style = {'width':'25%','display':'inline-block','vertical-align':'top'}),
		dbc.Col(content, style = {'width':'75%','display':'inline-block','top':'15px'})]
		    )


tab2_content = html.Div(
		[
		dbc.Col(sidebar_pred, style = {'width':'48%','display':'inline-block','vertical-align':'top'}),
		dbc.Col(content_pred, style = {'width':'48%','display':'inline-block','top':'15px'})]
		    )

tab0_content = html.Img(src='https://github.com/rasecotineb/data-project/blob/main/assets/resumen_proyecto.JPG',style={'width':'20%'}) #html.H5('Aquí irá un resumen del proyecto')
iframe_page1 = html.Iframe(src="https://datastudio.google.com/embed/reporting/614afda7-1ba7-4372-a9ca-56b450452c00/page/Z2XdB",
		style={'position':'absolute','top':'0','left':'0','width': '100%','height': '100%'})
tab_datastudio = html.Div(iframe_page1,style={'position': 'relative','padding-bottom':'56.25%','height': '0','overflow': 'hidden'})
iframe_page2 = html.Iframe(src="https://datastudio.google.com/embed/reporting/614afda7-1ba7-4372-a9ca-56b450452c00/page/9eqcB",
		style={'position':'absolute','top':'0','left':'0','width': '100%','height': '100%'})
tab_datastudio2 = html.Div(iframe_page2,style={'position': 'relative','padding-bottom':'56.25%','height': '0','overflow': 'hidden'})
tabs = dcc.Tabs(
    [
        dcc.Tab(tab0_content, label="Resumen de proyecto", style = TEXT_STYLE),
	dcc.Tab(tab_datastudio,label="Variables categóricas", style =TEXT_STYLE),
	dcc.Tab(tab_datastudio2,label="Correlación de variables", style =TEXT_STYLE),
        dcc.Tab(tab1_content, label="Resultados de modelos predictivo", style = TEXT_STYLE),
        dcc.Tab(tab2_content, label="Cálculo predictivo", style = TEXT_STYLE),
    ]
)

page = html.Div([
	html.Img(src='https://www.pucp.edu.pe/wp-content/themes/home-theme/images/logo-pucp.svg',style={'width':'20%'}),
	#dbc.NavbarSimple(
	#  children=[
	#    dbc.NavItem(dbc.NavLink("Colab",href="https://colab.research.google.com"))],
	#  brand="NavbarSimple",
	#  brand_href="",
	#  color="primary",
	#  dark=True	
	#),
        html.H2('Pronóstico de facturación mensual para bebidas gasificadas', style=TEXT_STYLE),
	html.H6('Diplomado en Data Analytics: Proyecto de Análisis de Datos', style=TEXT_STYLE),
	tabs
    ]
)

#-------------------------------------------------Configuración de variables--------------------------------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
server = app.server
app.layout = html.Div(page,style={'margin-left':'3%','margin-right':'3%','margin-top':'2%'})



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
    if 'Real' in dropdown_value:     
      dropdown_value.remove('Real')	
    return [generarMetricas(df, i, gastos_value) for i in dropdown_value]

@app.callback(
    Output('card_title_6', 'children'),
    [Input('predecir_button', 'n_clicks')],
    [State('dropdown_test', 'value'), State('input_cuota', 'value'), State('input_ingreso', 'value'),State('check_list', 'value')])
def update_card_title_6(n_clicks, dropdown_value, input_cuota, input_ingreso, check_list):
    print(check_list)
    result = generarFacturacion(parametros_df[parametros_df['algoritmo']==dropdown_value], input_cuota, input_ingreso,check_list)
    text_salida = 'Para ' + str(input_cuota) + ' botellas, con un ingreso bruto de ' + str(input_ingreso) + ','
    text_result = ' se estima una facturación de ' + str(result) + ' con el algoritmo ' + dropdown_value
    html_salida = html.P(text_salida + text_result)	
    return html_salida


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
