import requests
import pandas as pd

# Example API URL for fetching petrol prices
api_url = "https://api.fuelapi.in/api/v1/fuel-prices"

# Example API call (Replace with actual API URL and parameters)
response = requests.get(api_url, params={'state': 'kerala', 'fuel_type': 'petrol', 'api_key': 'YOUR_API_KEY'})

# Assuming the response is in JSON format
data = response.json()

# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
