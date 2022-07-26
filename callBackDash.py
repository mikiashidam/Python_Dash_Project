from math import prod
from turtle import color
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df1 = pd.read_csv("C:\\dataAnalytics\\combinedFolder.csv")
# print(df1.info())
# city_sales = df1.groupby('City').Purchase_Amount.sum()
# city_sales = pd.DataFrame(city_sales)
# city_sales.reset_index()
# print(city_sales)
# City = city_sales.index
# amount = city_sales.Purchase_Amount

# pivot = df.groupby(['City','month name']).Purchase_Amount.sum()

# pivot=pd.DataFrame(pivot)
# pivot.reset_index


# fig = px.bar(city_sales, x=City, y=amount, color=City, barmode="group")
# fig1 = px.line(city_sales)
# fig2 = px.line(pivot)

print(df1.columns)
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Dropdown(id="product-dropdown",
                 options=[
                     {"label": i, "value": i} for i in df1["Product"].unique()],
                 placeholder="Select a product",
                 multi=True
                 ),
    dcc.Dropdown(id="year-dropdown",
                 options=[
                     {"label": i, "value": i} for i in df1["Year"].unique()],
                 placeholder="Select a year",
                 multi=True
                 ),

    dcc.Graph(
        id='bar-graph',
        # figure=fig
    )
])


@app.callback(
    Output("bar-graph", "figure"),
    Input("product-dropdown", "value"),
    Input("year-dropdown", "value")
)
def display_graph(product, Year):
    # productdf = df1[df1["Product"] ==
    #                "product"][["month_name", "Purchase_Amount"]]
    if product == None:
        productdf = df1[df1["Product"] ==
                        "USB-C Charging Cable"][["month_name", "Purchase_Amount"]]
        productdf = productdf.groupby(
            "month_name").Purchase_Amount.sum().reset_index().sort_values(by="Purchase_Amount").head(500)
        # print(productdf.head)
        fig = px.bar(productdf, x=productdf.month_name,
                     y=productdf.Purchase_Amount, title="Bargraph for sales of USB-C Charging Cable", color=productdf.month_name)
        return fig
    else:
        productdf = df1[(df1["Product"].isin(
            product)) & (df1["Year"] == (Year))]  # sort_values(by="Purchase_Amount", ascending=False)
        productdf = productdf.groupby(
            "month_name").Purchase_Amount.sum().reset_index().sort_values(by="Purchase_Amount").head(500)
        print(productdf.head)
        fig = px.bar(productdf, x="month_name",
                     y="Purchase_Amount",
                     title=f"Bar graph for the sales of {product}", color=productdf.month_name)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
