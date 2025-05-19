from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata

df = pldata.gapminder(return_type="pandas", datetimes=True)
print(df)

# We create a Series of unique country names
countries = df["country"].drop_duplicates().sort_values()
print(countries)

# Initialize Dash app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in countries],
            value="Canada",
        ),
        dcc.Graph(id="gdp-growth"),
    ]
)


# Callback for dynamic updates
@app.callback(Output("gdp-growth", "figure"), [Input("country-dropdown", "value")])
def update_graph(country):
    # Filter the DataFrame for the chosen country
    df_filtered = df[df["country"] == country]

    fig = px.line(
        df_filtered,
        x="year",
        y="gdpPercap",
        title=f"GDP Per Capita Growth for {country}",
        labels={"year": "Year", "gdpPercap": "GDP per Capita"},
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
