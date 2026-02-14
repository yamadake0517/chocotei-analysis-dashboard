# Chocotei (Micro-stop) Analysis Dashboard

## Overview
This application analyzes frequent short equipment stops
("Chocotei") in manufacturing environments.

It helps identify:
- Which equipment stops most frequently
- Root cause distribution
- Stop rate per 1000 units
- Shift comparison
- Cause × Equipment heatmap

## Features
- KPI summary
- Equipment ranking
- Pareto analysis
- Monthly trend
- Shift comparison
- Heatmap visualization

## Tech Stack
- Python
- Streamlit
- Pandas
- Matplotlib

## How to Run

1. Install requirements:
pip install -r requirements.txt

2. Run:
streamlit run app0214.py


3. Upload sample_data/chocotei_sample_data.csv

## Note
This repository contains anonymized sample data only.
No confidential production data is included.