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

import google.cloud.bigquery as bigquery
from pathlib import Path
import importlib.util
import os


# Import settings file

MODULE_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
MODULE_PATH = MODULE_PATH.joinpath('query_sql.py')


# Load query_sql dynamically

WARE_LOAD = importlib.util.spec_from_file_location("query_sql", MODULE_PATH)
query_sql = importlib.util.module_from_spec(WARE_LOAD)
WARE_LOAD.loader.exec_module(query_sql)


# Define function get_data

def get_data(query):

    __client = bigquery.Client()

    __job = __client.query(query)

    return __job.result().to_dataframe()


if __name__ == '__main__':

    # Get query sql
    __query = query_sql.get_query()

    # Get data from BQ
    __data = get_data(__query)

    # Save data as data/data.csv
    __data.to_csv('../data/data.csv', index=False)

    # Save data as data in BQ
    # save_to_bq(__data, 'madrid-investing', 'DATA_LAKE_MODELING_US', 'data')
