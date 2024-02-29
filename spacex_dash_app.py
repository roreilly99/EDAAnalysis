# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'ALL'}]+[{'label': i, 'value': i} for i in launch_sites] , value='ALL', placeholder="place holder here", searchable=True
                                )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                                            marks={0: '0 (kg)',
                                                                                2500: '2500 (kg)',
                                                                                5000: '5000 (kg)',
                                                                                7500: '7500 (kg)',
                                                                                10000: '10,000 (kg)'},
                                                                            value=[min_payload, max_payload])
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        site_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts()
        total_successes = site_counts.sum()
        proportions = site_counts / total_successes
        fig = px.pie(names=proportions.index, values=proportions.values, title='Proportion of Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        successes_count = filtered_df[filtered_df['class'] == 1].shape[0]
        total_count = filtered_df.shape[0]
        success_proportion = successes_count / total_count
        fig = px.pie(values=[success_proportion, 1 - success_proportion], names=['Success', 'Failure'], title=f'Total Successes Launches for site {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(selected_site, payload_range):
    dataframe = spacex_df[spacex_df['Payload Mass (kg)'] > payload_range[0]]
    dataframe = dataframe[dataframe['Payload Mass (kg)'] < payload_range[1]]
    if selected_site == 'ALL':
        fig2 = px.scatter(dataframe, x = "Payload Mass (kg)", y = "class", color="Booster Version Category")
    else:
        filtered_df = dataframe[dataframe['Launch Site'] == selected_site]
        fig2 = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class", color="Booster Version Category")

    return fig2
# Run the app
if __name__ == '__main__':
    app.run_server()
