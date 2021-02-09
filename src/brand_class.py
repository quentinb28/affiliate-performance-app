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

from scipy import stats


# Define Brand class

class Brand:
    """Class to keep track of variant performance against control."""

    def __init__(self, group, test_period, kwargs):

        self.group = group
        self.test_period = test_period
        self.__dict__.update(kwargs)

    def chi2_test(self, __c):

        # Define significance level
        self.alpha = .05

        # Observations table: Impressions / Leads
        self.ob_table = [[__c.impressions_cum, __c.leads_cum],
                         [self.impressions_cum, self.leads_cum]]

        # Run chi square test and get chi square statistic and pvalue
        self.chisq, self.pvalue = stats.chi2_contingency(self.ob_table, correction=False)[:2]

        # Compute confidence level for the test
        self.confidence = f'{round(1 - self.pvalue, 2)*100}%'

        # Get test result
        self.result = 'significant' if self.pvalue < self.alpha else 'not significant'

    def uplift_potential(self, __c):

        # Compute ecpm uplift: control ecpm cum / variant ecpm cum
        self.ecpm_uplift = __c.ecpm_cum / self.ecpm_cum

        # Compute suggested rate
        # If the difference is significant
        # It means that one of them converts better
        # In that case, we multiply by the ecpm uplift
        if self.result == 'significant':

            self.suggested_rate = self.current_rate_converted * self.ecpm_uplift

        # If the difference is not significant
        # We consider both conversions are part of the same distributions
        else:

            # If the control rate is greater than the variant rate
            # We suggest the control rate for the variant rate
            if __c.current_rate_converted > self.current_rate_converted:

                self.suggested_rate = __c.current_rate_converted

            # If the variant rate is greater than the control rate
            # We do not suggest any updates
            else:

                self.suggested_rate = self.current_rate_converted

        # Compute suggested uplift: suggested rate / current rate
        self.suggested_uplift = self.suggested_rate / self.current_rate_converted

        # Compute daily uplift: potential revenue multiplied by effect size divided by test period
        self.daily_uplift = self.leads_cum * self.current_rate_converted * (self.suggested_uplift - 1) / self.test_period
