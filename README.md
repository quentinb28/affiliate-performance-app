<h1 align="center">
  Affiliate Performance Application
</p>

<img src="https://github.com/quentinb28/affiliate-performance-app/blob/main/images/affiliate-performance-app.gif" width=100%>

<p align="center">
 <img src="https://img.shields.io/badge/sql-v2017-pink.svg" />
 <img src="https://img.shields.io/badge/python-v3.7-yellow.svg" />
 <img src="https://img.shields.io/badge/pandas-v1.2-red.svg" />
 <img src="https://img.shields.io/badge/plotly-v4.14-purple.svg" />
 <img src="https://img.shields.io/badge/dash-v1.19-green.svg" />
 <img src="https://img.shields.io/badge/docker_image-v1-informational.svg" />
</p>

## Table of Contents

1. [Situation](#Situation)
2. [Techniques](#Techniques)
3. [Action](#Action)
4. [Results](#Results)
5. [Dash Deployment](#Dash-Deployment)
6. [Contributing](#Contributing)
7. [Licensing](#Licensing)

## 1. Situation

Investing.com is a financial platform and news website; one of the top three global financial websites in the world. It offers market quotes,information about stocks, futures, options, analysis, commodities, and an economic calendar. Most of the revenue is generated through advertising; Premium and Remnant. The Remnant business models are CPL / CPA / Networks. The best bidder fills the ad request. The objective is to maximize the profitability so we need to make all the alternatives comparable. To do that we compute the eCPM (Rate * Events * 1000 / Impressions). The higher the better.

## 2. Task

The project followed the following steps:

* Create a BigQuery table condensing the cumulative traffic data for each Site Geo, Brand.
* Perform in real-time statistical test to measure the performance of a Variant vs a Control.
* Build an Dash app that displays the performance in real-time.

## 3. Action

Firstly, the data was created based on the traffic data. Then a statistical test with alpha = 0.5 (Chi-Square test for independence) was performed between each Variant and the Control; the Control being defined as having the highest eCPM (Rate * Events * 1000 / Impressions) over the given perid. Filters were added for the traffic (Impressins + Click-Through Ratios) to adjust the results based on fair traffic allocations. The frequency of each category for one nominal variable is compared across the categories of the second nominal variable. Finally recommendatins were made to adjust rates based on the following conditions:

* Control conversion > Variant conversion and Significant: Variant Rate should be Variant Rate * eCPM uplift.
* Control conversion > Variant conversion and Not Significant: Variant Rate should be Control Rate.
* Variant conversion > Control conversion and Significant: Variant Rate should be Variant Rate * eCPM uplift.
* Variant conversion > Control conversion and Not Significant: Variant Rate should be Control Rate.

A Dash was built to display the performances in real-time and a Docker container was created for this app.

## 4. Results

The solution enables the team to prioritize and update the rates that represent the highest revenue uplifts on a daily basis.

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

## 6. Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

Please keep in mind that some of these projects might not be relevant anymore,
as our processes constantly evolve.

## 7. Licensing

Copyright © Investing.com . All rights reserved.
