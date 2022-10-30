from dash import Dash, html, dcc
from dash.dependencies import Input, Output
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
fig3 = px.histogram(df, x='year', y='gross', color='rating', barmode='group')

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Box Office Gross Data 1980-2020'),
        html.Div(children='''
            Box Office by Genre.
        '''),
        html.Label('Select Genre'),
        dcc.Dropdown(id= 'genre-dropdown', options=[{"value": i, "label": i} for i in genre_bo2['genre'].unique()],
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
        dcc.Dropdown(id= 'rating-dropdown', options=[{"value": i, "label": i} for i in rating_bo2['rating'].unique()],
                     value= ['G'], multi=True),
        dcc.Graph(
            id='display-selected-values-2',
            figure=fig2
        ), 
    ]),
    html.Div([
        html.H1(children='Gross per Rating by Year'),

        html.Div(),
        dcc.RangeSlider(
            min=df['year'].min(),
            max=df['year'].max(),
            step=None,
            marks={str(year): str(year) for year in df['year'].unique()},
            value=[df['year'].min(), df['year'].max()], id='rating-range-slider'
        ),
        dcc.Graph(
            id='display-selected-values-3',
            figure=fig3
        ),   
    ])
])


@app.callback(
    Output('display-selected-values', 'figure'),
    [Input('genre-dropdown', 'value')])
def update_output(value):
    ts = genre_bo2[genre_bo2["genre"].isin(value)]
    fig = px.line(ts, x="year", y="gross", color="genre", markers=True)
    return fig

@app.callback(
    Output('display-selected-values-2', 'figure'),
    [Input('rating-dropdown', 'value')])
def update_output2(value):
    ts = rating_bo2[rating_bo2["rating"].isin(value)]
    fig2 = px.line(ts, x="year", y="gross", color='rating', markers=True)
    return fig2

@app.callback(
    Output('display-selected-values-3', 'figure'),
    [Input('rating-range-slider', 'value')])
def update_output3(value):
    dff = df[df["year"].isin(value)]
    fig3 = px.histogram(dff, x='year', y='gross', color='rating', barmode='group')
    return fig3



if __name__ == '__main__':
    app.run_server(debug=True)