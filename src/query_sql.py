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


# Define function query_sql

def get_query():

    return '''

select 
  * 
from 
  (
    select 
      sitegeo, 
      DATE, 
      brand_name, 
      impressions, 
      clicks, 
      leads, 
      current_rate_converted, 
      deposits 
    from 
      (
        select 
          *, 
          max(date_wrong) over (partition by sitegeo) date_filter 
        from 
          (
            select 
              sitegeo, 
              DATE, 
              brand_name, 
              competitors_per_sitegeo_date, 
              case when competitors_per_sitegeo_date <> first_value(competitors_per_sitegeo_date) over (
                PARTITION BY sitegeo 
                ORDER BY 
                  DATE DESC
              ) then DATE else '2019-01-01' end date_wrong, 
              # get date if competitors count not relevant with current date or 2020-01-01
              lines_count, 
              impressions, 
              clicks, 
              leads, 
              current_rate_converted, 
              deposits 
            from 
              (
                select 
                  *, 
                  count(brand_name) over (partition by sitegeo, DATE) competitors_per_sitegeo_date 
                from 
                  (
                    -- compute brand_names count per sitegeo date
                    select 
                      concat(site, country_code) sitegeo, 
                      DATE, 
                      brand_name, 
                      max(current_rate_converted) current_rate_converted, 
                      count (*) lines_count, 
                      case when sum(impressions) = 0 
                      or sum(impressions) is null then 0 else sum(impressions) end impressions, 
                      case when sum(clicks) = 0 
                      or sum(clicks) is null then 0 else sum(clicks) end clicks, 
                      case when sum(leads) = 0 
                      or sum(leads) is null then 0 else sum(leads) end leads, 
                      case when sum(clicks) = 0 
                      or sum(clicks) is null then 0 else round(
                        sum(consolidated_revenue) / sum(clicks), 
                        2
                      ) end ecpc, 
                      case when sum(deposits) = 0 
                      or sum(deposits) is null then 0 else sum(deposits) end deposits, 
                    from 
                      `DATA_LAKE_MODELING_US.master_postback_ytd_current_rates_converted` 
                    where 
                      sales_sub_channel like 'Affiliation' 
                      and li_name not like '%_OASC_%' 
                      and li_name not like '%AdSense%'
                      and sales_sub_channel = 'Affiliation' 
                      and LENGTH(li_name) - LENGTH(
                        REGEXP_REPLACE(li_name, '_', '')
                      )>= 6 
                      and li_name like '%DFP' # select brand_names currently competing on a specific site geo
                      and concat(site, country_code, brand_name) in (
                        # Create type field (FC or Regular) and translate line_item_alias into brand names from SF
                        select 
                          distinct concat(site, country_code, brand_name) 
                        from 
                          `DATA_LAKE_MODELING_US.master_postback_ytd_current_rates_converted` 
                        where 
                          sales_sub_channel like 'Affiliation' 
                          and li_name not like '%_OASC_%' 
                          and li_name not like '%AdSense%'
                          and sales_sub_channel = 'Affiliation' 
                          and LENGTH(li_name) - LENGTH(
                            REGEXP_REPLACE(li_name, '_', '')
                          )>= 6 
                          and li_name like '%DFP' 
                          and DATE = current_date()
                          ) 
                    group by 
                      sitegeo, 
                      DATE, 
                      brand_name 
                    order by 
                      1 desc
                  )
              ) 
            order by 
              sitegeo, 
              DATE desc, 
              brand_name
          ) 
        order by 
          sitegeo, 
          DATE desc, 
          brand_name
      ) 
    where 
      DATE > date_filter 
    order by 
      sitegeo, 
      DATE desc, 
      brand_name
  ) 
where 
  DATE > date_add(
    current_date(), 
    interval -7 day
  )

    '''
