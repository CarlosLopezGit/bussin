import pandas as pd
import requests

# Replace with your actual stop ID (MonitoringRef)
stop_id = '550639'  # Example: 308209 is a Q49 stop

# API key and Stop Monitoring URL
api_key = ''
url = ('https://bustime.mta.info/api/siri/stop-monitoring.json?key=' + api_key + '&OperatorRef=MTA&MonitoringRef=' + stop_id + '&LineRef=MTABC_Q19')

# Make the request
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Navigate to the Stop Monitoring data
    visits = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']

    # Flatten the JSON and convert to a DataFrame
    df = pd.json_normalize(visits)

    # Save to CSV
    df.to_csv('stop_monitoring.csv', index=False)
    print("Stop monitoring data saved to stop_monitoring.csv")
else:
    print("Failed to fetch data:", response.status_code)