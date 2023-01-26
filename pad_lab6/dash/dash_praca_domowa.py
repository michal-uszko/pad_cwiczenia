from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('winequelity.csv').rename(columns={'Unnamed: 0': 'index'})


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'marginLeft': 'auto', 'marginRight': 'auto'})


app = Dash(__name__)

colors = {
    'background': '#3d3737',
    'text': '#f5f5f5'
}

app.layout = html.Div(
    children=[
        html.H2(children='Wines Data'),
        generate_table(df),

        html.Br(),
        html.Div(children=[
            html.Label(html.H2(children='Wybór modelu'),
                       ),
            dcc.RadioItems(['Regresja', 'Klasyfikacja'], 'Regresja', id='problem-radio')
        ],
        ),

        html.Br(),
        html.Div(children=[
            dcc.Dropdown(df.columns[1:],
                         'fixed acidity',
                         id='crossfilter-xaxis-column'
                         ),
            dcc.Graph(
                id='crossfilter-indicator-scatter'
            )
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}
        ),
    ], style={
        'verticalAlign': 'middle',
        'textAlign': 'center',
    },
)


@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('problem-radio', 'value'),
    Input('crossfilter-xaxis-column', 'value'))
def update_graph(value, xaxis_column_name):
    df_plot = df
    if value == 'Regresja':
        fig = px.scatter(x=df_plot[xaxis_column_name],
                         y=df_plot['pH']
                         )
        fig.update_xaxes(title=xaxis_column_name)
        fig.update_yaxes(title='pH')
    else:
        fig = px.box(data_frame=df_plot,
                     y=df_plot[xaxis_column_name],
                     x=df_plot['target'],
                     color='target'
                     )
        fig.update_yaxes(title=xaxis_column_name)
        fig.update_xaxes(title='target', type='category')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
