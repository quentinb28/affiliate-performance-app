# !/usr/bin/env python
# ! -*- coding: utf-8 -*-

"""
   Copyright © Investing.com
   Licensed under Private License.
   See LICENSE file for more information.
"""

#################################################

# Project: Create BQ table of Active Deals from Salesforce
# This file does the following:
# - retrieve all filtered product lines in Salesforce
# - organize and save them as a BQ table: sf_active_deals

#################################################


# Define function save_to_bq

def save_to_bq(df, project, dataset, filename):

    df.to_gbq(
        f'{dataset}.{filename}',
        if_exists='replace',
        project_id=project
    )
