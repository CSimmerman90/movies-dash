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
fig3 = px.histogram(df, x='year', y='gross', color='genre', barmode='group')

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
    html.Div([
        html.H1(children='Histogram of Gross by Genre per Year'),

        html.Div(),
        dcc.RangeSlider(
            min=1980,
            max=2020,
            step=None,
            marks={1980: '1980', 1981: '1981', 1982: '1982', 1983: '1983', 1984: '1984', 1985: '1985', 1986: '1986', 1987: '1987', 1988: '1988', 1989: '1989',
                   1990: '1990', 1991: '1991', 1992: '1992', 1993: '1993', 1994: '1994', 1995: '1995', 1996: '1996', 1997: '1997', 1998: '1998', 1999: '1999',
                   2000: '2000', 2001: '2001', 2002: '2002', 2003: '2003', 2004: '2004', 2005: '2005', 2006: '2006', 2007: '2007', 2008: '2008', 2009: '2009',
                   2010: '2010', 2011: '2011', 2012: '2012', 2013: '2013', 2014: '2014', 2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018', 2019: '2019', 2020: '2020' 
    },
    value=[1980, 2020], id='my-range-slider'
),
        dcc.Graph(
            id='display-selected-values-3',
            figure=fig3
        ),   
    ])
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

@app.callback(
    dash.dependencies.Output('display-selected-values-3', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output3(value):
    ts = df[df["year"].isin(value)]
    fig3 = px.histogram(ts, x="year", y="gross", color='genre', barmode='group')
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)