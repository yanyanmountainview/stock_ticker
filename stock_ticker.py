import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime as dt
from datetime import timedelta

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Enter a stock symbol:', style = {'paddingRight': '30px'}),
        dcc.Input(
            id = 'my_ticker_symbol',
            value = 'LRCX',
            style = {'fontSize':24, 'width': 75}
        )], style = {'display': 'inline-block', 'verticalAlgin': 'top'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id = 'my-date-picker-range',
            min_date_allowed = dt(2015, 1, 1),
            max_date_allowed = dt.today(),
            initial_visible_month= dt(2018, 1, 1),
            end_date = dt.today()
        )], style={'display':'inline-block'}),

    html.Div([
        html.Button(id = 'submit-button',
                    n_clicks = 0,
                    children = 'Submit',
                    style = {'fontSize': 24,
                            'marginLeft': '30px'})
    ], style = {'display': 'inline-block'}),
    dcc.Graph(
        id = 'my_graph',
        figure = {
            'data': [
                {'x':[1,2],
                 'y':[3,5]}
            ]
        }
    )
])

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = dt.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.strptime(end_date[:10], '%Y-%m-%d')
    df = web.DataReader(stock_ticker, 'iex', start, end)
    # Change the ouput datatime
    fig = {
        'data': [
            {'x': df.index, 'y': df.close}
        ],
        'layout': {'title': stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
