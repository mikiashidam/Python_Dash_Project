#from math import prod
#from turtle import color
#import dash_core_components as dcc
from dash import Dash, html, dcc, Input, Output, callback, State
import plotly.express as px
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
#import plotly.graph_objects as go

app = Dash(__name__)
conn = create_engine(
    'postgresql+psycopg2://postgres:tuja8817@127.0.0.1:5432/DVDRental')
sql1 = "select * from public.vw_top_n_sales"
salesdf1 = pd.read_sql_query(sql1, conn)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash-Postgres Demo'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Input(id="value_input",
              placeholder='Enter a value...',
              type='number',

              ),


    dcc.Graph(
        id='bar-graph',
        # figure=fig
    )
])


@app.callback(
    Output("bar-graph", "figure"),
    Input("value_input", "value")

)
def display_graph(value_input):

    totalSales = salesdf1.head(value_input)

    fig = px.bar(totalSales, x=totalSales["title"],
                 y="total_sales", title="Bargraph for total sales", color="total_sales")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
