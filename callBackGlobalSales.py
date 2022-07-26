import dash
from math import prod
from turtle import color
from unicodedata import category
from dash import Dash, html, dcc, Input, Output, State, callback, ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df1 = pd.read_csv("C:\\dataAnalytics\\GlobalSuperStore.csv")


most_profitable_cat = pd.pivot_table(df1[["Category", "Sales", "Profit_Margin"]], index=[
                                     "Category", "Sales", "Profit_Margin"], aggfunc="sum")
most_profitable_cat = most_profitable_cat.reset_index()
most_profitable_cat = most_profitable_cat.groupby(["Category"]).sum()
most_profitable_cat = most_profitable_cat.reset_index()
print(most_profitable_cat.head())

most_profitable_subCat = pd.pivot_table(df1[["Sub_Category", "Sales", "Profit_Margin"]], index=[
    "Sub_Category", "Sales", "Profit_Margin"], aggfunc="sum")
most_profitable_subCat = most_profitable_subCat.reset_index()
most_profitable_subCat = most_profitable_subCat.groupby(
    ["Sub_Category"]).sum()
most_profitable_subCat = most_profitable_subCat.reset_index()


most_profitable_subCat["Most_SubProfitable"] = most_profitable_subCat["Profit_Margin"]
most_profitable_subCat["Profitable_SubCategory"] = most_profitable_subCat["Sub_Category"]
most_profitable_cat["Profitable_Category"] = most_profitable_cat["Category"]
most_profitable_cat["Most_CatProfitable"] = most_profitable_cat["Profit_Margin"]


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Dropdown(id="Category-dropdown",
                 options=[
                     {"label": i, "value": i} for i in df1["Category"].unique()],
                 placeholder="Select a Category",
                 ),
    dcc.Dropdown(id="Sales-dropdown",
                 options=[
                     {"label": i, "value": i} for i in df1["Sales"].unique()],
                 placeholder="Select Profit_Margin",
                 ),
    dcc.RadioItems(id="ProfitCat-Button",
                   options=[
                       {"label": "ProfitabilityCat",
                           "value": "Most_CatProfitable"}
                   ],
                   value="Most_CatProfitable",
                   labelStyle={'display': 'none'}
                   ),
    dcc.RadioItems(id="ProfitSub-Button",
                   options=[
                       {"label": "ProfitabilitySub",
                           "value": "Most_SubProfitable"}
                   ],
                   value="Most_SubProfitable",
                   labelStyle={'display': 'none'}
                   ),
    dcc.RadioItems(id="SubCategory-Button",
                   options=[
                      {"label": "Most Profitable Sub_Category",
                       "value": "Profitable_SubCategory"},
                   ],
                   labelStyle={'width': '50%'}
                   ),
    dcc.RadioItems(id="Category-Button",
                   options=[
                       {"label": "Most Profitable Category",
                        "value": "Profitable_Category"}
                   ],
                   labelStyle={'width': '50%'}
                   ),
    html.Button(id="Button", n_clicks=0, children="Show breakdown"),
    dcc.Graph(
        id='bar-graph'
        # figure=fig
    )
])


@ app.callback(
    Output("bar-graph", "figure"),
    State("Category-dropdown", "value"),
    State("Sales-dropdown", "value"),
    State("ProfitSub-Button", "value"),
    State("SubCategory-Button", "value"),
    State("ProfitCat-Button", "value"),
    State("Category-Button", "value"),
    Input("Button", "n_clicks"),
    prevent_initial_call=True
)
# def update_graph(trig1,trig2):
#     triggered_id = ctx.triggered_id
#     if triggered_id == "Category-Button":
#         return display_graph1
def display_graph(category, City,  ProfitableSub, Subprofit, ProfitableCat, Catprofit, n):
    button_clicked = ctx.triggered_id
   # Which Category is Best Selling
    # if category == None:
    #     best_selling_pivot = pd.pivot_table(df1[["Category", "Sales", "Profit_Margin", "Product_Name"]], index=[
    #         "Category", "Profit_Margin", "Product_Name"], aggfunc="sum")
    #     best_selling_pivot = best_selling_pivot.reset_index()
    #     best_selling_pivot = best_selling_pivot.groupby(["Category"]).sum()

    #     best_selling_pivot = best_selling_pivot.reset_index()
    #     # best_selling_pivot.sort_values(by=["Profit_Margin"],
    #     #                                ascending=False).sort_values(by="Sales", ascending=False)

    #     # print(best_selling_pivot.head(100))
    #     fig = px.bar(best_selling_pivot, x="Category",
    #                  y="Sales", title="The best Selling Category", color=best_selling_pivot["Category"])
    #     return fig
    # elif category == category:
    #     best_selling_pivot = pd.pivot_table(df1[["Category", "Sub_Category", "Sales"]], index=[
    #         "Category", "Sub_Category"], aggfunc="sum")
    #     best_selling_pivot = best_selling_pivot.reset_index()
    #     best_selling_pivot = best_selling_pivot.groupby(
    #         ["Category", "Sub_Category"]).sum()

    #     best_selling_pivot = best_selling_pivot.reset_index()
    #     productdf = best_selling_pivot[best_selling_pivot["Category"] ==
    #                                    category]

    #     fig = px.bar(productdf, x="Sub_Category",
    #                  y="Sales", title=f"The Most {category} sold", color=productdf["Sub_Category"])
    #     return fig

    if Catprofit == 0:
        if Subprofit == 0:

            raise dash.exceptions.PreventUpdate

    elif n == 0:
        return ""

    elif Subprofit == Subprofit:

        fig = px.bar(most_profitable_subCat, x=Subprofit,
                     y=ProfitableSub, title=f"The Most {Subprofit} sold", color=Subprofit)
        return fig

    elif Catprofit == Catprofit:
        fig = px.bar(most_profitable_cat, x=Catprofit,
                     y=ProfitableCat, title=f"The Most {Catprofit}sold", color=most_profitable_cat["Category"])
        return fig

    print(n)


if __name__ == '__main__':
    app.run_server(debug=True)
