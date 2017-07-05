import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_csv('final_df_all_causes.csv')

risks = df['rei_name'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Markdown(
                children='#### Ensemble vs. Submission PAF Comparison')
        ], style={'width': '100%', 'display': 'inline-block',
                  'text-align': 'center'}),
        html.Div([
            html.Label('Risk'),
            dcc.Dropdown(
                id='risk',
                options=[{'label': i, 'value': i} for i in risks],
                value='Diet low in fruits'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Outcome'),
            dcc.Dropdown(
                id='cause',
                value='Ischemic heart disease'
            )
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([

        html.Div([
            dcc.Graph(id='paf-graphic-male')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='paf-graphic-female')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
])


@app.callback(
    dash.dependencies.Output('paf-graphic-male', 'figure'),
    [dash.dependencies.Input('risk', 'value'),
     dash.dependencies.Input('cause', 'value')])
def update_graph_male(selected_risk, selected_cause):

    filtered_df = df[df.rei_name == selected_risk]
    filtered_df = filtered_df[filtered_df.cause_name == selected_cause]
    max_ensemble = filtered_df['mean_ensemble'].max()
    max_submission = filtered_df['mean_submission'].max()
    if max_ensemble >= max_submission:
        max_paf_value = max_ensemble
    else:
        max_paf_value = max_submission
    max_paf_value += 0.02
    filtered_df = filtered_df[filtered_df.sex_id == 1]
    traces = []

    for i in filtered_df.super_region.unique():
        tmpdf = filtered_df[filtered_df['super_region'] == i]
        traces.append(go.Scatter(
            x=tmpdf['mean_ensemble'],
            y=tmpdf['mean_submission'],
            text=('Location: ' + tmpdf['location_name']),
            mode='markers',
            opacity=0.7,
            marker={
                'size': 7,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title='<b>Male, Age 55-59</b>',
            titlefont={'family': 'sans-serif',
                       'size': 13},
            xaxis={'range': [-0.01, max_paf_value],
                   'title': '<b>Ensemble PAF</b>',
                   'titlefont': {
                       'family': 'sans-serif',
                       'size': 10},
                   'tickfont': {
                       'family': 'sans-serif',
                       'size': 10}},
            yaxis={'range': [-0.01, max_paf_value],
                   'title': '<b>Submission PAF</b>',
                   'titlefont': {
                       'family': 'sans-serif',
                       'size': 10},
                   'tickfont': {
                       'family': 'sans-serif',
                       'size': 10}},
            shapes=[{'type': 'line',
                     'x0': 0,
                     'y0': 0,
                     'x1': 1,
                     'y1': 1,
                     'line': {
                         'color': 'rgb(128, 0, 128)',
                         'width': 2,
                         'dash': 'dot'}}],
            margin={'l': 50, 'b': 40, 't': 40, 'r': 10},
            legend={'orientation': 'h',
                    'x': 0,
                    'y': -0.15,
                    'font': {
                        'family': 'sans-serif',
                        'size': 10}},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('cause', 'options'),
    [dash.dependencies.Input('risk', 'value')])
def set_causes_options(selected_risk):

    filtered_df = df[df.rei_name == selected_risk]
    cause_list = filtered_df.cause_name.unique().tolist()

    return [{'label': i, 'value': i} for i in cause_list]


@app.callback(
    dash.dependencies.Output('paf-graphic-female', 'figure'),
    [dash.dependencies.Input('risk', 'value'),
     dash.dependencies.Input('cause', 'value')])
def update_graph_female(selected_risk, selected_cause):

    filtered_df = df[df.rei_name == selected_risk]
    filtered_df = filtered_df[filtered_df.cause_name == selected_cause]
    max_ensemble = filtered_df['mean_ensemble'].max()
    max_submission = filtered_df['mean_submission'].max()
    if max_ensemble >= max_submission:
        max_paf_value = max_ensemble
    else:
        max_paf_value = max_submission
    max_paf_value += 0.02
    filtered_df = filtered_df[filtered_df.sex_id == 2]
    traces = []

    for i in filtered_df.super_region.unique():
        tmpdf = filtered_df[filtered_df['super_region'] == i]
        traces.append(go.Scatter(
            x=tmpdf['mean_ensemble'],
            y=tmpdf['mean_submission'],
            text=('Location: ' + tmpdf['location_name']),
            mode='markers',
            opacity=0.7,
            marker={
                'size': 7,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title='<b>Female, Age 55-59</b>',
            titlefont={'family': 'sans-serif',
                       'size': 13},
            xaxis={'range': [-0.01, max_paf_value],
                   'title': '<b>Ensemble PAF</b>',
                   'titlefont': {
                       'family': 'sans-serif',
                       'size': 10},
                   'tickfont': {
                       'family': 'sans-serif',
                       'size': 10}},
            yaxis={'range': [-0.01, max_paf_value],
                   'title': '<b>Submission PAF</b>',
                   'titlefont': {
                       'family': 'sans-serif',
                       'size': 10},
                   'tickfont': {
                       'family': 'sans-serif',
                       'size': 10}},
            shapes=[{'type': 'line',
                     'x0': 0,
                     'y0': 0,
                     'x1': 1,
                     'y1': 1,
                     'line': {
                         'color': 'rgb(128, 0, 128)',
                         'width': 2,
                         'dash': 'dot'}}],
            margin={'l': 50, 'b': 40, 't': 40, 'r': 10},
            legend={'orientation': 'h',
                    'x': 0,
                    'y': -0.15,
                    'font': {
                        'family': 'sans-serif',
                        'size': 10}},
            hovermode='closest'
        )
    }


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


if __name__ == '__main__':
    app.run_server(
        host="0.0.0.0",
        port=8050,
        debug=True
    )
