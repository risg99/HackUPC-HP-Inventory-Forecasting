import pandas as pd
import datetime
from datetime import datetime
from dash import Dash, Input, Output, dcc, html

dataDF = (
	pd.read_csv('data/preprocessed_train.csv')
)

products = dataDF["product_number"].sort_values().unique()
segments = dataDF["segment"].sort_values().unique()
productCategories = dataDF["prod_category"].sort_values().unique()

myStyleSheet = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]


app = Dash(__name__, external_stylesheets = myStyleSheet)
app.title = "HP Analytics!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
            
                html.P(children=html.Img(src=app.get_asset_url("favicon.ico")), className="header-emoji"),
                html.H1(
                    children="HP Analytics: Understand Your Inventory!", className="header-title"
                ),
                html.P(
                    children=(
                        "Welcome to HP Analytics. Enter your requirements here to identify the estimated inventory levels...."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                        children=[
                            html.Div(children = "Product", className = "menu-title"),
                            dcc.Dropdown(
                                id = "product-filter",
                                options = [
                                    {"label" : productVar, "value" : productVar}
                                    for productVar in products
                                ],
                                value = "...",
                                clearable = True,
                                className = "dropdown",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(children = "Segment", className = "menu-title"),
                            dcc.Dropdown(
                                id = "segment-filter",
                                options = [
                                    {"label" : segmentVar, "value" : segmentVar}
                                    for segmentVar in segments
                                ],
                                value = "...",
                                clearable = True,
                                className = "dropdown",
                            ),
                        ]
                    ),
                    html.Div(
                        children = [
                            html.Div(children = "Product Category", className = "menu-title"),
                            dcc.Dropdown(
                                id = "prodCat-filter",
                                options = [{"label" : prodCat, "value" : prodCat} 
                                    for prodCat in productCategories
                                ],
                                value = "...",
                                clearable = True,
                                className = "dropdown",
                            ),
                        ],
                    ),
                    html.Div(
                        children = [
                            html.Div(children = "Date Range", className = "menu-title"),
                            dcc.DatePickerRange(
                                id = "date-range",
                                # min_date_allowed = data["date"].min(),
                                # max_date_allowed = data["date"].max(),
                                start_date = dataDF["date"].min(),
                                end_date = dataDF["date"].max(),
                            ),
                        ]
                    ),
                ],
                className = "menu",
            ),
            html.Div(
                children = [
                    html.Div(
                            dcc.Graph(
                                id = "inventory-units",
                                config={"displayModeBar": False},
                            ),
                            className = "card",
                        ),
                    ],
                    className = "wrapper",
                ),
        ],
    )

@app.callback(
        Output("inventory-units","figure"),
        Input("product-filter","value"),
        Input("segment-filter","value"),
        Input("prodCat-filter","value"),
        Input("date-range","start_date"),
        Input("date-range","end_date"),
    )

def update_charts(productVar, segmentVar, productCategoryVar, startDateVar, endDateVar):
    global dataDF

    startDate = datetime.strptime(startDateVar,'%Y-%m-%d').date()
    endDate = datetime.strptime(endDateVar,'%Y-%m-%d').date()

    startYear = startDate.year
    endYear = endDate.year

    startWeek = startDate.isocalendar()[1]
    endWeek = endDate.isocalendar()[1]

    startString = startYear*100 + int(startWeek)
    endString = endYear*100 + int(endWeek)

    filtered_data = dataDF.query(
            "product_number == @productVar and segment == @segmentVar and prod_category == @productCategoryVar and year_week >= @startString and year_week <= @endString"
        )

    inventory_units_figure = {
        "data": [
            {
                "x": filtered_data["year_week"][:10],
                "y": filtered_data["inventory_units"][:10],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Inventory Levels at HP",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return inventory_units_figure

if __name__ == "__main__":
    app.run_server(debug=True)