#from math import prod
#from turtle import color
from dash import Dash, html, dcc, Input, Output, callback, State
import plotly.express as px
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
#import plotly.graph_objects as go

app = Dash(__name__)
conn = create_engine(
    'postgresql+psycopg2://postgres:tuja8817@127.0.0.1:5432/DVDRental')
catSql = "select * from public.vw_distinct_film_category"
catdf = pd.read_sql_query(catSql, conn)

citySql = "select * from public.vw_distinct_city"
citydf = pd.read_sql_query(citySql, conn)

monthSql = "select * from public.vw_get_payment_month"
monthdf = pd.read_sql_query(monthSql, conn)

salesSQl = "select * from public.sales_by_film_category"
salesdf = pd.read_sql_query(salesSQl, conn)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash-Postgres Demo'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Dropdown(id="category-dropdown",
                 options=[
                     {"label": i, "value": i} for i in catdf["name"]],
                 placeholder="Select a category",
                 multi=True
                 ),
    dcc.Dropdown(id="city-dropdown",
                 options=[
                     {"label": i, "value": i} for i in citydf["city"]],
                 placeholder="Select a city",
                 multi=True
                 ),

    dcc.Dropdown(id="month-dropdown",
                 options=[
                     {"label": i, "value": i} for i in monthdf["month"]],
                 placeholder="Select a month",
                 multi=True
                 ),

    dcc.Graph(
        id='bar-graph',
        # figure=fig
    )
])


@app.callback(
    Output("bar-graph", "figure"),
    State("category-dropdown", "value"),
    State("city-dropdown", "value"),
    Input("month-dropdown", "value")

)
def display_graph(category, city, month):

    if category == None:

        # print(productdf.head)
        fig = px.bar(salesdf, x="category",
                     y="total_sales", title="Bargraph for total sales", color="category")
        return fig
    else:
        # print('checking city type')
        # print(type(city))
        #         sql1 = f"""
        #    SELECT c.name AS category,
        #     sum(p.amount) AS total_sales,
        #     trim(to_char(p.payment_date,'MONTH')) as sales_month,
        #     ct.city
        #    FROM payment p
        #      JOIN rental r ON p.rental_id = r.rental_id
        #      JOIN inventory i ON r.inventory_id = i.inventory_id
        #      JOIN film f ON i.film_id = f.film_id
        #      JOIN film_category fc ON f.film_id = fc.film_id
        #      JOIN category c ON fc.category_id = c.category_id
        #      JOIN customer cus ON cus.customer_id=p.customer_id
        #      JOIN address ad ON ad.address_id=cus.address_id
        #      JOIN city ct ON ct.city_id=ad.city_id
        #      WHERE trim(to_char(p.payment_date,'MONTH'))::Character(30)=trim('{month}')
        #      AND ct.city='{city}'
        #     GROUP BY c.name,sales_month,ct.city
        #     ORDER BY (sum(p.amount)) DESC;
        #     """
        sql1 = "select * from public.vw_category_month"
        salesdf1 = pd.read_sql_query(sql1, conn)
        salesdf1 = salesdf1[(salesdf1["city"] == city) &
                            (salesdf1["month"] == month)]
        print(salesdf1.head())

    fig = px.bar(salesdf1, x="category",
                 y="total_sales", title="Bargraph for total sales", color="category")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
