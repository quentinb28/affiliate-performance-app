# Affiliate Performance Application
![Python](https://img.shields.io/badge/python-v3.7-yellow.svg)
![Pandas](https://img.shields.io/badge/pandas-v1.2-orange.svg)
![Plotly](https://img.shields.io/badge/plotly-v4.14-red.svg)
![Dash](https://img.shields.io/badge/dash-v1.19-purple.svg)
![Docker](https://img.shields.io/badge/docker_image-v1-blue.svg)

## Basic Overview
<img src="https://github.com/quentinb28/affiliate-performance-app/blob/main/images/affiliate-performance-app.gif" width=100%>

## Table of Contents

1. [Project Objectives](#Project-Objectives)
2. [Resources / Tools](#Resources-/-Tools)
3. [Data Collection](#Data-Collection)
4. [Statistical Test](#Statistical-Test)
5. [Dash Deployment](#Dash-Deployment)
6. [Contributing](#Contributing)
7. [Licensing](#Licensing)

## 1. Project Objectives

* Collect affiliate data in a relevant time period.
* Compare performances based on sound statistical tests.
* Display results in an easy-to-read application.
* Suggest rate adjustments to maximize revenues.

## 2. Resources / Tools

* Google BigQuery (SQL)
* Python
* Pandas
* Plotly
* Dash
* Docker

## 3. Data Collection

* Collect last-7-days data with converted rates: [SQL Query](https://github.com/quentinb28/affiliate-performance-app/blob/main/src/query_sql.py)
* Load data from BigQuery to Dataframe: [Get Data](https://github.com/quentinb28/affiliate-performance-app/blob/main/src/get_data.py)

## 4. Statistical Test

* Filter unbalanced delivery (Daily Impressions / Click-Through Rates)
* Pick control brand based on cumulated effective Cost Per Mile (eCPM).
* Run ChiSquare Test for Independance on conversion rate between variant and control (Leads / Impressions).
* Suggest relevant rate based on test results:
  * Significant Difference: Variant Rate * eCPM uplift
  * Not Significant Difference: Control Rate (if Control Rate > Variant Rate)

## 5. App Deployment

### Dockerfile

```
FROM python:3.7
ADD . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
```

### Pull Docker Image (Not Public Yet)

```
docker pull quentinb28/affiliate-performance-app:latest
```

### Run Docker Container

```
docker run -name affiliate-performance-app -p 8080:8080 quentinb28/affiliate-performance-app:latest
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

Please keep in mind that some of these projects might not be relevant anymore,
as our processes constantly evolve.

## Licensing

Copyright © Investing.com . All rights reserved.
