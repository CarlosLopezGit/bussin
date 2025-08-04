import numpy
import pandas as pd
import requests
from datetime import datetime

# Replace with your actual stop ID (MonitoringRef)
stop_id = '550639'  # Example: 308209 is a Q49 stop

# API key and Stop Monitoring URL
api_key = '658e51bf-62ec-4533-b5c0-dac9918143c4'
url = ('https://bustime.mta.info/api/siri/stop-monitoring.json?key=' + api_key + '&OperatorRef=MTA&MonitoringRef=' + stop_id + '&LineRef=MTABC_Q19')

# Make the requestpy
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

    # Grab the arrival times column,
    arrival_times = df['MonitoredVehicleJourney.MonitoredCall.AimedArrivalTime'] 

    # Get the current time
    now = datetime.now().astimezone()

    #loop throught the arrival times and print arrival info
    for i in arrival_times:

        #format arrival time from iso format
        arrival = datetime.fromisoformat(i)

        # Calcualte time left before bus arrives
        time_left = arrival - now

        #Convert time left into minutes as int
        mins_left = int(time_left.total_seconds() // 60)

        print('Q19 bus coming at ')
        # print formatted time as str and remaining minutes
        print((arrival.strftime('%I:%M:%S %p')) + ('... in %d minutes' % mins_left))
        print()
    
else:
    print("Failed to fetch data:", response.status_code)