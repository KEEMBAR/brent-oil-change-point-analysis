# Brent Oil Change Point Analysis

This project analyzes the impact of major geopolitical and economic events on Brent oil prices using Bayesian change point detection. The goal is to provide actionable insights for investors, policymakers, and energy companies by identifying structural breaks in oil price time series and associating them with key global events.

## Project Structure

```
brent-oil-change-point-analysis/
├── data/
│   └── raw/
│       └── BrentOilPrices.csv
│   └── events.csv
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── data_preparation.py
│   ├── change_point_model.py
│   └── utils.py
├── dashboard/
│   ├── backend/
│   └── frontend/
├── requirements.txt
├── README.md
└── .gitignore

## What Has Been Done

- Data cleaning and exploratory data analysis (EDA) on historical Brent oil prices (1987-2022)
- Compiled a comprehensive dataset of major events affecting the oil market
- Analyzed time series properties: trend, stationarity, and volatility clustering
- Documented key assumptions and limitations of the analysis

## Next Steps

- Implement Bayesian change point detection using PyMC3
- Identify and interpret significant change points in the price series
- Quantify the impact of major events on price regimes
- Build an interactive dashboard (Flask + React) to visualize results for stakeholders

```
