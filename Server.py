cty2iso = {
    "Germany": "DEU",
    "Uruguay": "URY",
    "Italy": "ITA",
    "England": "GBR",
    "Brazil": "BRA", 
    "Argentina": "ARG",
    "France": "FRA",
    "Spain": "ESP"
}
import numpy as np
import pandas as pd
import plotly as plt
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px


data = pd.read_csv("data.csv")
data.drop(22,inplace=True)
ctys = []
for cty in data["Winners"]:
    ctys.append(cty2iso[cty])

data = data.assign(iso=pd.Series(ctys))
data.head()
gpdta = data.groupby(by=["Winners","iso"], as_index =False)["Score"].count()

fig = px.choropleth(gpdta, locations='iso',
                    color="Score", # number of wins
                    hover_name="Winners", # column to add to hover information
                    )
app = Dash()
app.layout = [html.Header(children='World Cup Winners', style={'textAlign':'center'}),
            dcc.Dropdown(data.Year, 1930, id="ddyear"),
              html.Div(id='Runner-Up'),
              dcc.Graph(figure = fig),
]
@callback(
    Output(component_id='Runner-Up', component_property='children'),
    Input(component_id='ddyear', component_property='value')
)
def update_output_div(inp):
    ind = data.index[data['Year'] == inp]
    Ru =(data.iat[3, 3])
    return f'Runner Up: {Ru}'

if __name__ == '__main__':
    app.run(debug=True)