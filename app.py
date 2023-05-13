import datetime
from datetime import datetime
from dash import Dash, Input, Output, dcc, html, dash_table
import query

products, segments, productCategories, dates = query.get_hp_data()

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
                                start_date = dates.min(),
                                end_date = dates.max(),
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
            html.Div(
                children = [ 
                    html.Div(
                            id='inventory-units-table-card',
                            children = [   
                                html.Div(
                                    children = [
                                        html.H3(
                                            f"Data Table",
                                            style = {
                                                "display": "inline-block"
                                            }
                                        ),
                                        # html.
                                        html.Button("Export Table", id="export_table",                    
                                        style={
                                            "fontSize": "1em",
                                            "background-color": "white",
                                            "color": "black",
                                            "border-radius": "5px",
                                            "border": "2px none",
                                            "box-shadow": '0px 0px 2px 2px rgb(0,0,0)',
                                            'display': 'inline-block',
                                            'float':'right',
                                            'margin-top':'1em',
                                            'padding': '6px'
                                            
                                        })
                                    ],
                                ),          
                                html.Div(
                                    dash_table.DataTable(
                                        id = 'inventory-units-table',
                                        style_header={
                                            "backgroundColor": "#00a6999c",
                                            "color": "black",
                                            "fontWeight":"bold"
                                        },
                                        style_data={"backgroundColor": "#fcfcfc", "color": "black"},
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': '#00a69947',
                                            }
                                        ],
                                        style_cell={'textAlign': 'center'},
                                        editable=False,
                                        filter_action="native",
                                        
                                        sort_action="native",
                                        sort_mode="multi",
                                        page_action="native",
                                        page_current=0,
                                        page_size=10,
                                        export_format="csv",
                                        export_headers= 'display'
                                    ),
                                    className = "card"
                                )
                            ],
                            hidden= True,
                            className = "wrapper",
                        ),
                    
                    ],
                    className = "wrapper",
                ),
        ],
    )

@app.callback(
        Output("inventory-units","figure"),
        Output("inventory-units-table",'data'),
        Output("inventory-units-table",'columns'),
        Output("inventory-units-table-card",'hidden'),
        Input("product-filter","value"),
        Input("segment-filter","value"),
        Input("prodCat-filter","value"),
        Input("date-range","start_date"),
        Input("date-range","end_date")
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

    now = datetime.now()
    thisYear = now.year
    thisWeek = now.isocalendar()[1]

    if( (startYear <= thisYear) or (startYear == thisYear and int(startWeek) <= int(thisWeek)) ):
        filtered_data = query.get_history().query(
                "product_number == @productVar and segment == @segmentVar and prod_category == @productCategoryVar and year_week >= @startString and year_week <= @endString"
            )
    else:
        todayString = thisYear*100 + int(thisWeek)
        ## pass required parameters
        filtered_data = query.predict()

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

    table_data = filtered_data[['product_number','year_week','sales_units','inventory_units']]\
            .rename(columns={'product_number':'Product','year_week': 'Year & Week',\
                             'sales_units': 'Forecasted Sales','inventory_units':'Forecasted Inventory'}).astype('str')
    hidden = table_data.empty

    return inventory_units_figure, \
        table_data.to_dict('rows'), [
      {"name": i, 'id': i} for i in table_data.columns
   ], hidden

## Export table function
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0)
            document.querySelector("#inventory-units-table button.export").click()
        return ""
    }
    """,
    Output("export_table", "data-dummy"),
    [Input("export_table", "n_clicks")]
)

if __name__ == "__main__":
    app.run_server(debug=True)