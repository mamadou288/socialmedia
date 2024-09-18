import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load data
data = pd.read_csv("assets/socialmedia_waisters.csv")

app = dash.Dash(__name__)

# App layout with updated CSS classes for S-tier design
app.layout = html.Div(children=[
    # Header
    html.H1(children='Social Media Dashboard'),
    
    # Dropdown for selecting multiple platforms
    dcc.Dropdown(
        id='platform-dropdown',
        options=[
            {'label': 'Instagram', 'value': 'Instagram'},
            {'label': 'TikTok', 'value': 'TikTok'},
            {'label': 'Facebook', 'value': 'Facebook'},
            {'label': 'YouTube', 'value': 'YouTube'}
        ],
        value=['Instagram'],  # Default value is Instagram
        multi=True,  # Allow multi-selection
        className='dropdown'
    ),
    
    # Graphs container
    html.Div(className='graph-container', children=[
        html.Div(dcc.Graph(id='scroll-rate-graph'), className='graph-box'),
        html.Div(dcc.Graph(id='gender-distribution-graph'), className='graph-box'),
        html.Div(dcc.Graph(id='age-average-graph'), className='graph-box'),
        html.Div(dcc.Graph(id='debt-count-graph'), className='graph-box'),
        html.Div(dcc.Graph(id='engagement-graph'), className='graph-box')
    ])
])

# Callback to update the scroll rate graph based on selected platforms
@app.callback(
    Output('scroll-rate-graph', 'figure'),
    [Input('platform-dropdown', 'value')]
)
def update_scroll_rate_graph(selected_platforms):
    scroll_rate_data = {platform: data[data['Platform'] == platform]['Scroll Rate'].mean() for platform in selected_platforms}
    
    fig = go.Figure(data=[
        go.Bar(name=platform, x=[platform], y=[scroll_rate_data[platform]]) for platform in selected_platforms
    ])
    
    fig.update_layout(
        title='Average Scroll Rate',
        xaxis_title='Platform',
        yaxis_title='Scroll Rate',
        plot_bgcolor='#2c2f4c',  # Dark background
        paper_bgcolor='#2c2f4c',
        font_color='#f5f5f5'
    )
    
    return fig

@app.callback(
    Output('gender-distribution-graph', 'figure'),
    [Input('platform-dropdown', 'value')]
)
def update_gender_distribution_graph(selected_platforms):
    fig = go.Figure()
    for platform in selected_platforms:
        gender_data = data[data['Platform'] == platform]['Gender'].value_counts()
        fig.add_trace(go.Bar(name=f'{platform} Male', x=[platform], y=[gender_data.get('Male', 0)]))
        fig.add_trace(go.Bar(name=f'{platform} Female', x=[platform], y=[gender_data.get('Female', 0)]))
    
    fig.update_layout(
        barmode='group',
        title='Gender Distribution',
        xaxis_title='Platform',
        yaxis_title='Count',
        plot_bgcolor='#2c2f4c',
        paper_bgcolor='#2c2f4c',
        font_color='#f5f5f5'
    )
    
    return fig

@app.callback(
    Output('age-average-graph', 'figure'),
    [Input('platform-dropdown', 'value')]
)
def update_age_average_graph(selected_platforms):
    age_data = {platform: data[data['Platform'] == platform]['Age'].mean() for platform in selected_platforms}
    
    fig = go.Figure(data=[
        go.Bar(name=platform, x=[platform], y=[age_data[platform]]) for platform in selected_platforms
    ])
    
    fig.update_layout(
        title='Average Age',
        xaxis_title='Platform',
        yaxis_title='Age',
        plot_bgcolor='#2c2f4c',
        paper_bgcolor='#2c2f4c',
        font_color='#f5f5f5'
    )
    
    return fig

@app.callback(
    Output('debt-count-graph', 'figure'),
    [Input('platform-dropdown', 'value')]
)
def update_debt_count_graph(selected_platforms):
    debt_data = {platform: data[data['Platform'] == platform]['Debt'].sum() for platform in selected_platforms}
    
    fig = go.Figure(data=[
        go.Bar(name=platform, x=[platform], y=[debt_data[platform]]) for platform in selected_platforms
    ])
    
    fig.update_layout(
        title='Debt Count',
        xaxis_title='Platform',
        yaxis_title='Users in Debt',
        plot_bgcolor='#2c2f4c',
        paper_bgcolor='#2c2f4c',
        font_color='#f5f5f5'
    )
    
    return fig

@app.callback(
    Output('engagement-graph', 'figure'),
    [Input('platform-dropdown', 'value')]
)
def update_engagement_graph(selected_platforms):
    engagement_data = {platform: data[data['Platform'] == platform]['Engagement'].mean() for platform in selected_platforms}
    
    fig = go.Figure(data=[
        go.Bar(name=platform, x=[platform], y=[engagement_data[platform]]) for platform in selected_platforms
    ])
    
    fig.update_layout(
        title='Average Engagement',
        xaxis_title='Platform',
        yaxis_title='Engagement',
        plot_bgcolor='#2c2f4c',
        paper_bgcolor='#2c2f4c',
        font_color='#f5f5f5'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
