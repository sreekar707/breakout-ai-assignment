# Cryptocurrency Price Prediction Project

This project predicts future price movements for a specified cryptocurrency based on historical data. Using the CryptoCompare API, it fetches historical data and calculates features that serve as inputs for a machine learning model (Random Forest Regressor). The model is trained to forecast future price variations using these derived features.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Data Collection](#data-collection)
4. [Feature Engineering](#feature-engineering)
5. [Model Training](#model-training)
6. [Installation and Usage](#installation-and-usage)

## Project Overview

This project aims to predict short-term future highs and lows for a cryptocurrency using machine learning. It focuses on the following steps:
- Fetching historical cryptocurrency data.
- Calculating relevant metrics based on historical price movements.
- Training a model to predict future price changes based on these metrics.

## Features

- **Data Collection**: Fetches historical cryptocurrency data using the CryptoCompare API.
- **Feature Engineering**: Calculates historical and future metrics, such as the percentage difference from recent highs/lows and days since last high/low.
- **Model Training**: Trains a Random Forest Regressor to predict future price movements based on these engineered features.

## Data Collection

The `fetch_crypto_data()` function retrieves historical price data from the CryptoCompare API for a given cryptocurrency asset within a specified date range. Data is fetched in daily intervals, and the API limits are handled by fetching the data in chunks.

### Example of Data Fetched
| Date       | Open     | High     | Low      | Close    |
|------------|----------|----------|----------|----------|
| 2023-10-01 | 1482.5   | 1500.8   | 1470.2   | 1490.1   |

## Feature Engineering

The `calculate_metrics()` function calculates relevant features based on the fetched data:
- **Historical High and Low Metrics**:
  - `%_Diff_From_High_Last_7_Days`: Percentage difference between the current close and the highest price in the last 7 days.
  - `Days_Since_High_Last_7_Days`: Days since the last highest price within the last 7 days.
- **Future High and Low Metrics**:
  - `%_Diff_From_High_Next_5_Days`: Percentage difference between the current close and the highest price in the next 5 days.
  - `Days_Since_Low_Last_7_Days`: Days since the last lowest price within the last 7 days.

These metrics are designed to help the model capture trends and anticipate short-term price movements.

## Model Training

The model training process involves:
1. **Data Splitting**: Splitting the data into training and testing sets.
2. **Training**: Initial training of a RandomForestRegressor model.
3. **Evaluation**: Using Mean Squared Error (MSE) and Mean Absolute Error (MAE) to evaluate model accuracy.
4. **Hyperparameter Tuning**: Using GridSearchCV to optimize parameters for better model performance.

### Model Performance
The final model's performance is evaluated using the Mean Squared Error (MSE) and Mean Absolute Error (MAE) on the test set.

## Installation and Usage

### Prerequisites
- Python 3.8 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/crypto-price-prediction.git
   cd crypto-price-prediction

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the script file:
   ```bash
   python cryptui.py
4. Run the model file :