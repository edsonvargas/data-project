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
      resolucion = 'ACEPTABLE'
    else:
      style_card = CARD_NOT_ACCEPTABLE_STYLE
      resolucion = 'NO ACEPTABLE' 			 
    return html.P(value + ' es un ' + str(precision) + '% preciso, con un BV = S/.' +
			str(bv) + ' [' + resolucion +'] ', style=style_card)

def generarFacturacion(df_params,cuota,ingreso,check_list):
    result = cuota * df_params['Cuota C.U'].values[0] +  ingreso * df_params['Ing. Bruto  Cuota S/. Mensual'].values[0]	
    result2 = ingreso * df_params['Ing. Neto  Cuota S/.  Mensual'].values[0] + df_params['intercepto'].values[0]
    if check_list is not None: 
      for i in check_list:
        result2 = result2 + df_params[i].values[0]
    return (result+result2)/100

def build_intro():
    return html.Div(
        id='intro',
        children=[
            html.Img(src='assets/resumen_proyecto.JPG'),
        ],
    )

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
    'color': '#666666'
}

CARD_ACCEPTABLE_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
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
        html.P('Cantidad de Cajas Unitarias', style=CARD_TEXT_STYLE),
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
	  dbc.Col(html.P('Número de cajas unitarias', style=CARD_TEXT_STYLE),md=6),
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
        md=8
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
        md=4
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
            dcc.Graph(id='graph_5'), md=8
        ),
        dbc.Col([
	    html.Br(),
	    html.Div("El Business Value (BV), expresa la cantidad de recursos logísticos adicionales en los que incurrirá el negocio luego de 				pronosticar una facturación. El BV ideal es S/. 0, sin embargo, dada la variación del mercado, se permite un 15% de 				gastos adicionales, según la experiencia del negocio", style=CARD_TEXT_STYLE),
	    html.Br(),			
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
            )], md=4
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

tab3_recursos = html.Div(
		[
		html.Br(),
		html.H6("Recursos utilizados en esta presentación:", style=CARD_TEXT_STYLE),
		html.Br(),
		html.Li("Ruta de Notebook realizado en Colaboratory Google:"),
		html.A("Ver", href='https://colab.research.google.com/drive/1bzPJdhejIXfb6sDRR4QUbv_r-AgL0uP7?usp=sharing'),
		html.Li("Ruta de la presentación de proyecto de análisis de datos"),
		html.A("Ver", href='https://drive.google.com/file/d/1B_AsyMxjRrVN-MgExN0sgVEtU0ZaqlKP/view?usp=sharing'),
		html.Li("Ruta de repositorio Github de este dashboard"),
		html.A("Ver", href='https://github.com/edsonvargas/data-project'),
		html.Li("Tutorial de carga de Dashboard a Google Cloud Platform"),
		html.A("Ver", href='https://datasciencecampus.github.io/deploy-dash-with-gcp/')],
		style={'margin-left':'15%'}
		    )

tab0_content = build_intro()
iframe_page1 = html.Iframe(src="https://datastudio.google.com/embed/reporting/614afda7-1ba7-4372-a9ca-56b450452c00/page/Z2XdB",
		style={'position':'absolute','top':'0','left':'0','width': '100%','height': '100%'})
tab_datastudio = html.Div(iframe_page1,style={'position': 'relative','padding-bottom':'56.25%','height': '0','overflow': 'hidden'})
iframe_page2 = html.Iframe(src="https://datastudio.google.com/embed/reporting/614afda7-1ba7-4372-a9ca-56b450452c00/page/9eqcB",
		style={'position':'absolute','top':'0','left':'0','width': '100%','height': '100%'})
tab_datastudio2 = html.Div(iframe_page2,style={'position': 'relative','padding-bottom':'56.25%','height': '0','overflow': 'hidden'})

subtabs = dcc.Tabs(
    [
	dcc.Tab(tab_datastudio,label="Variables categóricas", style =TEXT_STYLE),
	dcc.Tab(tab_datastudio2,label="Correlación de variables", style =TEXT_STYLE)
    ]
)


tabs = dcc.Tabs(
    [
        dcc.Tab(tab0_content, label="Resumen de proyecto", style = TEXT_STYLE),
	dcc.Tab(subtabs,label="Análisis estadístico", style =TEXT_STYLE),
        dcc.Tab(tab1_content, label="Análisis predictivo", style = TEXT_STYLE),
        dcc.Tab(tab2_content, label="Interacción de modelos", style = TEXT_STYLE),
	dcc.Tab(tab3_recursos, label="Recursos Adicionales", style = TEXT_STYLE),
    ]
)

page = html.Div([
	html.Img(src='https://raw.githubusercontent.com/edsonvargas/data-project/main/data/logo-pucp.svg',style={'width':'20%'}),
        html.H2('Pronóstico de facturación mensual para bebidas gasificadas', style=TEXT_STYLE),
	html.H6('Diplomado en Data Analytics: Proyecto de Análisis de Datos', style=TEXT_STYLE),
	tabs
    ]
)

#-------------------------------------------------Configuración de variables--------------------------------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
server = app.server
app.layout = html.Div(page,style={'margin-left':'3%','margin-right':'3%','margin-top':'2%'})


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
			range_y=[mintarget,maxtarget],labels={"Cuota C.U": "# Cajas Unitarias"},color_discrete_map={"Modelo Regresion":"#030f6f","Real":"#A7A7A7","Modelo Ridge":"#49baff","Modelo Lasso":"#0f557f","Modelo Huber":"black"})
    return fig


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
    text_salida = 'Para ' + str(input_cuota) + ' cajas unitarias, con un ingreso bruto de S/.' + str(input_ingreso) + ','
    text_result = ' se estima una facturación de S/.' + str(result) + ', con el algoritmo de ' + dropdown_value
    html_salida = html.P(text_salida + text_result)	
    return html_salida


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
