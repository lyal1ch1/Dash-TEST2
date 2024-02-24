import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('./spacex_launch_dash.csv')

app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])


app.layout = html.Div([
    html.H1("SpaceX Launch", style={'textAlign': 'center'}),
    html.H2("Select Launch Site:"),
    dcc.Dropdown(
        id='launch-site-dropdown',
        options=[
            {'label': 'Все стартовые площадки', 'value': 'all'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        ],
        value='all'
    ),
    html.Label("Payload Range:"),
    dcc.RangeSlider(
        id='payload-range-slider',
        min=0,
        max=10000,
        step=100,
        marks={i: str(i) for i in range(0, 10001, 500)},
        value=[0, 10000]
    ),
    html.Div(id='output-graphs')
], className="container" )

# Определение функций обратного вызова для обновления графиков при взаимодействии пользователя
@app.callback(
    Output('output-graphs', 'children'),
    [Input('launch-site-dropdown', 'value'),
     Input('payload-range-slider', 'value')]
)   
def update_graphs(selected_launch_site, payload_range):
    filtered_df = df
     
    # Фильтрация данных в зависимости от выбранных параметров
    if selected_launch_site != 'all':
        filtered_df = filtered_df[df['Стартовая площадка'] == selected_launch_site]
    
    filtered_df = filtered_df[(filtered_df['Масса полезной нагрузки (kg)'] >= payload_range[0]) & 
                              (filtered_df['Масса полезной нагрузки (kg)'] <= payload_range[1])]
    
    # Создание круговой диаграммы
    pie_chart = px.pie(filtered_df, names='Стартовая площадка', title='Успешные запуски')
    
    
    scatter_chart = px.scatter(filtered_df, x='Масса полезной нагрузки (kg)', y='Стартовая площадка', color='Стартовая площадка', 
                           title='Масса полезной нагрузки в зависимости от места запуска')


    return [
        dcc.Graph(figure=pie_chart),
        dcc.Graph(figure=scatter_chart)
    ]

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
