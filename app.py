import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('movies.csv')
genre_bo = df.drop(['name','rating', 'released', 'score', 'votes', 'director', 'writer', 'star', 'country', 'budget', 'company', 'runtime'], axis=1)
genre_bo2 = genre_bo.groupby(['genre', 'year'])['gross'].sum().reset_index(name='gross')

rating_bo = df.drop(['name','genre', 'released', 'score', 'votes', 'director', 'writer', 'star', 'country', 'budget', 'company', 'runtime'], axis=1)
rating_bo2 = rating_bo.groupby(['rating', 'year'])['gross'].sum().reset_index(name='gross')

fig = px.line(genre_bo2, x="year", y="gross", color='genre', markers=True)
fig2 = px.line(rating_bo2, x="year", y="gross", color='rating', markers=True)

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Box Office by Genre'),
        html.Div(children='''
            Analysis of Movie Data.
        '''),
        html.Label('Select Genre'),
        dcc.Dropdown(id= 'demo-dropdown', options=[{"value": i, "label": i} for i in genre_bo2['genre'].unique()],
                     value= ['Action'], multi=True),
        dcc.Graph(
            id='display-selected-values',
            figure=fig
        ),
    ]),
    html.Div([
        html.H1(children='Box Office by Rating'),

        html.Div(),
        html.Label('Select Rating'),
        dcc.Dropdown(id= 'demo2-dropdown', options=[{"value": i, "label": i} for i in rating_bo2['rating'].unique()],
                     value= ['G'], multi=True),
        dcc.Graph(
            id='display-selected-values-2',
            figure=fig2
        ), 
    ]),
])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    ts = genre_bo2[genre_bo2["genre"].isin(value)]
    fig = px.line(ts, x="year", y="gross", color="genre", markers=True)
    return fig

@app.callback(
    dash.dependencies.Output('display-selected-values-2', 'figure'),
    [dash.dependencies.Input('demo2-dropdown', 'value')])
def update_output2(value):
    ts = rating_bo2[rating_bo2["rating"].isin(value)]
    fig2 = px.line(ts, x="year", y="gross", color='rating', markers=True)
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)