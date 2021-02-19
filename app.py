# !/usr/bin/env python
# ! -*- coding: utf-8 -*-

"""
   Copyright © Investing.com
   Licensed under Private License.
   See LICENSE file for more information.
"""

#################################################

# Project: Affiliate Performance Optimisation
# A/B Test - Affiliation Campaigns
# Based on Chi-Square statistical test, alpha=.05

#################################################


# Libraries

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from src.brand_class import Brand

# Define constants

ROW_SCHEMA = dict(sitegeo='',
                  test_period='',
                  group='',
                  brand_name='',
                  current_rate_converted='',
                  impressions_cum='',
                  clicks_cum='',
                  ctr_cum='',
                  leads_cum='',
                  ltr_cum='',
                  deposits_cum='',
                  ecpm_cum='',
                  ecpa_cum='',
                  confidence='',
                  alpha='',
                  result='',
                  ecpm_uplift='',
                  suggested_rate='',
                  suggested_uplift='',
                  daily_uplift='')

BY_COLS = ['sitegeo', 'brand_name']

FOR_COLS = ['impressions', 'clicks', 'leads', 'deposits']

ORDER_BY_COLS = ['DATE']

ROUND_COLS = ['ecpm_cum', 'ecpa_cum', 'ecpm_uplift', 'suggested_rate', 'suggested_uplift', 'daily_uplift']


# Helper functions

def filter_delivery(df, tol_imps=100, tol_ctr=100):
    """
    Objective: Filter out dates where delivery unbalances greater than inputs
    :param df: Dataframe
    :param tol_imps: tolerance impressions in percentage * 100
    :param tol_ctr: tolerance ctr in percentage * 100
    :return: Dataframe with relevant dates
    """

    out_dates = []

    for __d in df.DATE.unique():

        max_imps = df.loc[df['DATE'] == __d, 'impressions'].max()
        min_imps = df.loc[df['DATE'] == __d, 'impressions'].min()
        diff_imps_perc = (max_imps - min_imps) / max_imps

        max_ctr = df.loc[df['DATE'] == __d, 'ctr'].max()
        min_ctr = df.loc[df['DATE'] == __d, 'ctr'].min()
        diff_ctr_perc = (max_ctr - min_ctr) / max_ctr

        if diff_imps_perc * 100 > tol_imps or diff_ctr_perc * 100 > tol_ctr:
            out_dates.append(__d)

    return df[~df['DATE'].isin(out_dates)]


def make_cumsum_cols(df, by_cols=None, for_cols=None, order_by_cols=None):
    """
    Objective: Create cumulative columns based on input
    :param df: Dataframe
    :param by_cols: Columns to group by
    :param for_cols: Columns to compute from
    :param order_by_cols: Columns to order by
    :return: Dataframe with new columns
    """

    df_sorted = df.sort_values(by=order_by_cols, ascending=True)

    for __c in for_cols:
        df_sorted[f'{__c}_cum'] = df_sorted.groupby(by=by_cols)[__c].transform(lambda x: x.cumsum())

    return df_sorted


def abt_function(df):
    """
    Objective: Run a Chi Square test for a specific country between control and variant(s)
    :param df: Dataframe filtered by sitegeo
    :return: Dataframe with Chi Square Results
    """

    rows = []

    # Filter info last day with cumulative info
    __df_last = df[df['DATE'] == df['DATE'].max()]

    # Compute test period
    __test_period = len(df['DATE'].unique())

    # Instantiate control brand
    __control = Brand('control', __test_period, __df_last.loc[__df_last['ecpm_cum'].idxmax()].to_dict())

    # Create copy of row schema for control row
    __control_row = ROW_SCHEMA.copy()

    # Build control row from control brand object attributes
    for attr, value in __control.__dict__.items():
        if attr in __control_row:
            __control_row[attr] = value

    rows.append(__control_row)

    # Iterate through variants
    for __v in [__v for __v in __df_last['brand_name'].unique() if __v != __control.brand_name]:

        # Instantiate variant brand
        __variant = Brand('variant', __test_period, __df_last.loc[__df_last['brand_name'] == __v].to_dict('records')[0])

        # Run chi square test against control
        __variant.chi2_test(__control)

        # Compute uplift metrics
        __variant.uplift_potential(__control)

        # Create copy of row schema for variant row
        __variant_row = ROW_SCHEMA.copy()

        # Build control row from variant brand object attributes
        for attr, value in __variant.__dict__.items():
            if attr in __variant_row:
                __variant_row[attr] = value

        rows.append(__variant_row)

    return pd.DataFrame(rows)


def filter_no_variants(df):
    """
    Objective: Filter out sitegeos where there are no variants
    :param df: Dataframe with all sitegeos
    :return: Dataframe with sitegeos having at least one variant
    """

    # Filter info last day
    __df_last = df[df['DATE'] == df['DATE'].max()]

    # Group by sitegeo, count brands
    __df_grouped = __df_last.groupby(by='sitegeo', as_index=False).brand_name.count()

    filter_sitegeos = []

    # Add sitegeos that have no variants
    for _ in range(len(__df_grouped)):

        if __df_grouped.loc[_, 'brand_name'] < 2:
            filter_sitegeos.append(__df_grouped.loc[_, 'sitegeo'])

    return df[~df['sitegeo'].isin(filter_sitegeos)]


def filter_no_leads(df):
    """
    Objective: Filter out sitegeos where there are no leads
    :param df: Dataframe with all sitegeos
    :return: Dataframe with sitegeos having at least one lead
    """

    # Group by sitegeo, count brands
    __df_grouped = df.groupby(by='sitegeo', as_index=False).leads.sum()

    filter_sitegeos = []

    # Add sitegeos that have no variants
    for _ in range(len(__df_grouped)):

        if __df_grouped.loc[_, 'leads'] < 1:
            filter_sitegeos.append(__df_grouped.loc[_, 'sitegeo'])

    return df[~df['sitegeo'].isin(filter_sitegeos)]


# Load df

df = pd.read_csv('data/data.csv')

# Filter out sitegeos with no variants

df = filter_no_variants(df)

# Instantiate dash app

app = dash.Dash()

# Create app layout

app.layout = html.Div([

    # Header Div
    html.Div([

        # Title Div
        html.H1('A/B Test - Affiliation Campaigns',
                style={'textAlign': 'center',
                       'fontSize': 40,
                       'fontWeight': 'bold',
                       'marginTop': 0,
                       'marginBottom': 0}),

        # Background image Div
        html.Div([

        ], style={'height': 240, 'background-image': 'url("assets/animals_cropped.jpg")', 'border': 'solid black'}),

        # Filters Div
        html.Div([

            html.Div([

                html.Div([

                    html.H3('Impressions Tolerance % (Daily)'),

                    dcc.Slider(id='my_slider_tolerance_impressions_picker',
                               min=1,
                               max=100,
                               value=5,
                               marks={int(n): str(int(n)) for n in np.linspace(0, 100, 6)}
                               ),

                ], style={'display': 'inline-block', 'verticalAlign': 'Top', 'width': '20%', 'marginRight': '50px'}),

                html.Div([

                    dcc.Dropdown(id='my_dropdown_sitegeo_picker',
                                 options=[{'label': __c, 'value': __c} for __c in df['sitegeo'].fillna('').unique()],
                                 value='UKGB'
                                 ),

                ], style={'display': 'inline-block', 'marginTop': 30, 'width': '20%', 'textAlign': 'center',
                          'border': 'solid red'}),

                html.Div([

                    html.H3('CTR Tolerance % (Daily)'),

                    dcc.Slider(id='my_slider_tolerance_ctr_picker',
                               min=1,
                               max=100,
                               value=25,
                               marks={int(n): str(int(n)) for n in np.linspace(0, 100, 6)}
                               ),

                ], style={'display': 'inline-block', 'verticalAlign': 'Top', 'width': '20%', 'marginLeft': '50px'}),

            ], style={'textAlign': 'center', 'borderBottom': 'solid black'}),

        ]),

    ]),

    # Performance Graph Div
    html.Div([

        dcc.Graph(id='performance_graph',
                  figure={})

    ], style={'height': 400}),

    # Performance Table Div
    html.Div([

        dt.DataTable(id='performance_table',
                     columns=[{'name': c, 'id': c} for c in ROW_SCHEMA.keys()],
                     data=[],
                     sort_action='native',
                     filter_action='native')

    ], style={'marginTop': 0})

])


@app.callback(Output('performance_graph', 'figure'),
              [Input('my_dropdown_sitegeo_picker', 'value'),
               Input('my_slider_tolerance_impressions_picker', 'value'),
               Input('my_slider_tolerance_ctr_picker', 'value')])
def update_performance_graph(sitegeo, tol_imps, tol_ctr):

    # Filter df with sitegeo from input
    df_sitegeo = df.loc[df['sitegeo'] == sitegeo]

    # Create daily ctr to filter big gaps in delivery
    df_sitegeo['ctr'] = df_sitegeo['clicks'] / df_sitegeo['impressions']

    # Filter df with tolerance impressions / ctr from input
    df_filtered = filter_delivery(df_sitegeo, tol_imps=tol_imps, tol_ctr=tol_ctr)

    # Filter out sitegeos with no leads
    df_filtered = filter_no_leads(df_filtered)

    # If df empty from filter then return empty figure
    if df_filtered.empty:
        return {}

    # Create cumulative values for relevant columns
    df_cumsum = make_cumsum_cols(df_filtered, by_cols=BY_COLS, for_cols=FOR_COLS, order_by_cols=ORDER_BY_COLS)

    # Create cumulative ecpm based on current rate converted to USD
    df_cumsum['ecpm_cum'] = df_cumsum['leads_cum'] * df_cumsum['current_rate_converted'] * 1000 / df_cumsum[
        'impressions_cum']

    # Add relevant traces for the performance graph
    data = []

    for __brand_name in df_cumsum['brand_name'].unique():
        # Line traces for cumulative eCPM
        data.append(go.Scatter(
            x=df_cumsum.loc[df_cumsum['brand_name'] == __brand_name, :]['DATE'],
            y=df_cumsum.loc[df_cumsum['brand_name'] == __brand_name, :]['ecpm_cum'],
            legendgroup=__brand_name,
            name=__brand_name,
            yaxis='y1'
        ))

        # Bar traces for cumulative impressions
        data.append(go.Bar(
            x=df_cumsum.loc[df_cumsum['brand_name'] == __brand_name, :]['DATE'],
            y=df_cumsum.loc[df_cumsum['brand_name'] == __brand_name, :]['impressions_cum'],
            legendgroup=__brand_name,
            name=__brand_name,
            yaxis='y2',
            opacity=0.3
        ))

    # Compose figure
    figure = {'data': data,
              'layout': {'title': 'Delivery Performance Over Test Period (Days)',
                         'yaxis': {'title': 'Cumulative eCPM (USD)'},
                         'yaxis2': {'title': 'Cumulative Delivery (Impressions)', 'side': 'right', 'overlaying': 'y'},
                         'legend': {'orientation': 'h', 'x': 0.8, 'y': 1.4},
                         'height': 400}}

    return figure


@app.callback(Output('performance_table', 'data'),
              [Input('my_dropdown_sitegeo_picker', 'value'),
               Input('my_slider_tolerance_impressions_picker', 'value'),
               Input('my_slider_tolerance_ctr_picker', 'value')])
def update_performance_table(sitegeo, tol_imps, tol_ctr):

    # Filter df with sitegeo from input
    df_sitegeo = df.loc[df['sitegeo'] == sitegeo]

    # Create daily ctr to filter big gaps in delivery
    df_sitegeo['ctr'] = df_sitegeo['clicks'] / df_sitegeo['impressions']

    # Filter df with tolerance impressions / ctr from input
    df_filtered = filter_delivery(df_sitegeo, tol_imps=tol_imps, tol_ctr=tol_ctr)

    # Filter out sitegeos with no leads
    df_filtered = filter_no_leads(df_filtered)

    # If df empty from filter then return None
    if df_filtered.empty:
        return None

    # Create cumulative values for relevant columns
    df_cumsum = make_cumsum_cols(df_filtered, by_cols=BY_COLS, for_cols=FOR_COLS, order_by_cols=ORDER_BY_COLS)

    # Compute cumulated ctr
    df_cumsum['ctr_cum'] = round(df_cumsum['clicks_cum'] / df_cumsum['impressions_cum'] * 100000, 2)

    # Compute cumulated ltr
    df_cumsum['ltr_cum'] = round(df_cumsum['leads_cum'] / df_cumsum['impressions_cum'] * 100000, 2)

    # Compute cumulated ecpm
    df_cumsum['ecpm_cum'] = df_cumsum['leads_cum'] * df_cumsum['current_rate_converted'] * 1000 / df_cumsum[
        'impressions_cum']

    # Compute cumulated ecpa
    df_cumsum['ecpa_cum'] = df_cumsum['leads_cum'] * df_cumsum['current_rate_converted'] / df_cumsum[
        'deposits_cum']

    # Run abt function
    df_abt = abt_function(df_cumsum)

    for __c in ROUND_COLS:
        df_abt[__c] = df_abt[__c].apply(lambda x: round(x, 2) if isinstance(x, float) else x)

    return df_abt.to_dict('records')


# Execute application on server

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
