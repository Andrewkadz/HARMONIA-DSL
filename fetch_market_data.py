import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json
import csv
import os

def fetch_data(symbol, filename):
    client = ApiClient()
    print(f"Fetching data for {symbol}...")
    
    try:
        # Fetch 5 years of daily data
        response = client.call_api('YahooFinance/get_stock_chart', query={
            'symbol': symbol,
            'region': 'US',
            'interval': '1d',
            'range': '5y',
            'includeAdjustedClose': True
        })
        
        if response and 'chart' in response and 'result' in response['chart']:
            result = response['chart']['result'][0]
            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]
            
            # Prepare CSV data
            rows = []
            for i in range(len(timestamps)):
                if quotes['close'][i] is not None:
                    rows.append({
                        'timestamp': timestamps[i],
                        'open': quotes['open'][i],
                        'high': quotes['high'][i],
                        'low': quotes['low'][i],
                        'close': quotes['close'][i],
                        'volume': quotes['volume'][i]
                    })
            
            # Save to CSV
            filepath = f"/home/ubuntu/HARMONIA-DSL/{filename}"
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                writer.writeheader()
                writer.writerows(rows)
                
            print(f"Saved {len(rows)} records to {filepath}")
            return True
        else:
            print(f"No data found for {symbol}")
            return False
            
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        return False

if __name__ == "__main__":
    # Fetch Bitcoin
    fetch_data('BTC-USD', 'btc_data.csv')
    
    # Fetch S&P 500
    fetch_data('^GSPC', 'spx_data.csv')
