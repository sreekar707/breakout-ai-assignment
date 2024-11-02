import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_crypto_data(asset_id, start_date, end_date):
    # Convert dates to timestamps
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    
    # Set the API parameters
    max_limit = 2000
    all_data = []
    current_timestamp = end_timestamp
    
    # Fetch data in chunks until we reach the start date
    while current_timestamp >= start_timestamp:
        # Set the API URL with the current timestamp and limit
        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={asset_id}&tsym=USD&toTs={current_timestamp}&limit={max_limit}'
        
        # Make the API request
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            return pd.DataFrame()
        
        # Parse the JSON data
        data = response.json().get('Data', {}).get('Data', [])
        
        if not data:
            print("No data returned; either limit exceeded or data unavailable.")
            break
        
        # Filter out data before start_timestamp
        filtered_data = [d for d in data if d['time'] >= start_timestamp]
        
        # Append the filtered data to our list
        all_data.extend(filtered_data)
        
        # Update current_timestamp to be one day before the earliest timestamp in this chunk
        current_timestamp = data[0]['time'] - 86400  # Move back by one day
        
        # Break if we've reached or gone past the start date
        if current_timestamp < start_timestamp:
            break
    
    # Convert the data to a DataFrame
    if not all_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_data)
    
    # Convert timestamp to datetime
    df['date'] = pd.to_datetime(df['time'], unit='s')
    
    # Rename columns to match required output
    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close"
    })
    
    # Select the desired columns and sort by date in ascending order
    df = df[['date', 'Open', 'High', 'Low', 'Close']].sort_values(by="date").reset_index(drop=True)
    
    # Filter the final DataFrame to ensure we only have data within our date range
    df = df[
        (df['date'].dt.date >= datetime.strptime(start_date, "%Y-%m-%d").date()) &
        (df['date'].dt.date <= datetime.strptime(end_date, "%Y-%m-%d").date())
    ]
    
    return df

def calculate_metrics(data, variable1, variable2):
    # Calculate Historical High Price and Days Since High
    data[f'High_Last_{variable1}_Days'] = data['High'].rolling(window=variable1, min_periods=1).max()
    data[f'Days_Since_High_Last_{variable1}_Days'] = (
        data['High'].rolling(window=variable1, min_periods=1)
        .apply(lambda x: (variable1 - 1) - x[::-1].argmax())
    )
    
    # Calculate % Difference from Historical High
    data[f'%_Diff_From_High_Last_{variable1}_Days'] = (
        (data['Close'] - data[f'High_Last_{variable1}_Days']) / data[f'High_Last_{variable1}_Days'] * 100
    )
    
    # Calculate Historical Low Price and Days Since Low
    data[f'Low_Last_{variable1}_Days'] = data['Low'].rolling(window=variable1, min_periods=1).min()
    data[f'Days_Since_Low_Last_{variable1}_Days'] = (
        data['Low'].rolling(window=variable1, min_periods=1)
        .apply(lambda x: (variable1 - 1) - x[::-1].argmin())
    )
    
    # Calculate % Difference from Historical Low
    data[f'%_Diff_From_Low_Last_{variable1}_Days'] = (
        (data['Close'] - data[f'Low_Last_{variable1}_Days']) / data[f'Low_Last_{variable1}_Days'] * 100
    )
    
    # Calculate Future High Price and % Difference from Future High
    data[f'High_Next_{variable2}_Days'] = data['High'].shift(-variable2).rolling(window=variable2, min_periods=1).max()
    data[f'%_Diff_From_High_Next_{variable2}_Days'] = (
        (data['Close'] - data[f'High_Next_{variable2}_Days']) / data[f'High_Next_{variable2}_Days'] * 100
    )
    
    # Calculate Future Low Price and % Difference from Future Low
    data[f'Low_Next_{variable2}_Days'] = data['Low'].shift(-variable2).rolling(window=variable2, min_periods=1).min()
    data[f'%_Diff_From_Low_Next_{variable2}_Days'] = (
        (data['Close'] - data[f'Low_Next_{variable2}_Days']) / data[f'Low_Next_{variable2}_Days'] * 100
    )
    
    return data

# Example usage
if __name__ == "__main__":
    asset_id = 'BTC'  # Cryptocurrency symbol
    start_date = '2017-10-01'
    end_date = datetime.now().strftime('%Y-%m-%d') 
    
    df = fetch_crypto_data(asset_id, start_date, end_date)
    
    # Calculate metrics
    variable1 = 7 
    variable2 = 5  
    df_with_metrics = calculate_metrics(df, variable1, variable2)
    
    print(df_with_metrics)
    
df_with_metrics.to_csv('crypto_data_with_metrics.csv', index=False)

print("Data saved to 'crypto_data_with_metrics.csv'")

