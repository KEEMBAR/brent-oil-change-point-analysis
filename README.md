# Brent Oil Change Point Analysis

This project analyzes the impact of major geopolitical and economic events on Brent oil prices using Bayesian change point detection. The goal is to provide actionable insights for investors, policymakers, and energy companies by identifying structural breaks in oil price time series and associating them with key global events.

## Project Structure

brent-oil-change-point-analysis/
├── data/
│ ├── raw/
│ │ └── BrentOilPrices.csv
│ ├── events.csv
│ └── changepoints.csv
├── notebooks/
│ └── eda.ipynb
├── src/
│ ├── data_preparation.py
│ ├── change_point_model.py
│ └── utils.py
├── dashboard/
│ ├── backend/
│ │ ├── app.py
│ │ └── routes/
│ │ ├── changepoints.py
│ │ ├── events.py
│ │ └── prices.py
│ └── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Dashboard.js
│ │ │ ├── EventFilter.js
│ │ │ ├── PriceChart.js
│ │ │ └── VolatilityChart.js
│ │ └── ...
│ └── package.json
├── requirements.txt
├── README.md
└── .gitignore

---

## What Has Been Done

- Cleaned and explored historical Brent oil prices data (1987-2022) with detailed EDA.
- Compiled and curated a dataset of significant geopolitical, economic, and OPEC events affecting oil prices.
- Analyzed time series properties, including trends, stationarity, and volatility clustering.
- Implemented a Bayesian change point detection model using PyMC3 to identify structural breaks in oil prices.
- Statistically linked detected change points to key global events and quantified their impact on price regimes.
- Developed a fully interactive dashboard with:
  - Flask backend serving APIs for prices, events, change points, and summary statistics.
  - React frontend providing intuitive charts and filtering options for stakeholder exploration.
- Ensured cross-origin resource sharing (CORS) and smooth integration between backend and frontend.
- Documented key assumptions, limitations, and communicated insights tailored for investors, policymakers, and energy companies.

## Key Features of the Dashboard

- Interactive visualizations of Brent oil prices and volatility over time.
- Highlighted major geopolitical and economic events affecting the market.
- Markers for Bayesian-detected change points and structural breaks.
- Filtering tools to focus on specific event types or time ranges.
- Summary statistics providing quick insights on overall market behavior.

## Acknowledgements

Special thanks to the tutorial team: Mahlet, Rediet, Kerod, and Rehmet, whose guidance helped shape this analysis.
