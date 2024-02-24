import dash
from dash import dcc, html, Input, Output
import requests
import plotly.express as px

# Функция для получения курсов валют относительно базовой валюты
def get_exchange_rates(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    print(data['rates'])
    return data['rates']

# Функция для создания гистограммы курсов валют
def create_histogram(base_currency):
    rates = get_exchange_rates(base_currency)
    df = {'Валюта': list(rates.keys()), 'Курс': list(rates.values())}
    fig = px.histogram(df, x="Валюта", y="Курс", log_y=True)
    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Курс валют и конвертер", style={'textAlign': 'center'}),
    html.Label("Выберите базовую валюту:"),
    dcc.Dropdown(
        id='base-currency-dropdown',
        options=[
            {'label': 'USD', 'value': 'USD'},
            {'label': 'EUR', 'value': 'EUR'},
            {'label': 'GBP', 'value': 'GBP'},
            {'label': 'RUB', 'value': 'RUB'},
        ],
        value='USD'
    ),
    html.Div([
        html.Label("Конвертер валют:"),
        dcc.Input(id='input-amount', type='number', value=1),
        dcc.Dropdown(
            id='target-currency-dropdown',
            options=[
                {'label': 'USD', 'value': 'USD'},
                {'label': 'EUR', 'value': 'EUR'},
                {'label': 'GBP', 'value': 'GBP'},
                {'label': 'RUB', 'value': 'RUB'},
            ],
            value='EUR'
        ),
        html.Button('Конвертировать', id='submit-button', n_clicks=0),
        html.Div(id='output-converted-amount')
    ]),
    dcc.Graph(id='exchange-rate-histogram'),
])

@app.callback(
    Output('exchange-rate-histogram', 'figure'),
    [Input('base-currency-dropdown', 'value')]
)
def update_histogram(base_currency):
    fig = create_histogram(base_currency)
    return fig

@app.callback(
    Output('output-converted-amount', 'children'),
    [Input('submit-button', 'n_clicks')],
    [Input('input-amount', 'value')],
    [Input('base-currency-dropdown', 'value')],
    [Input('target-currency-dropdown', 'value')]
)
def convert_currency(n_clicks, amount, base_currency, target_currency):
    if n_clicks > 0:
        rates = get_exchange_rates(base_currency)
        converted_amount = amount * rates[target_currency]
        return f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"

if __name__ == '__main__':
    app.run_server(debug=True)
