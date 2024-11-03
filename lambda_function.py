import json
import requests
import boto3
import os
import time
from datetime import datetime

# Initialize the S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Fetch environment variables
        api_key = os.environ['API_KEY']  # Set this environment variable in Lambda
        bucket_name = os.environ['BUCKET_NAME']  # Set this environment variable in Lambda

        # List of Indian capitals
        indian_capitals = [
            "Amaravati", "Itanagar", "Dispur", "Patna", "Raipur", "Panaji",
            "Gandhinagar", "Chandigarh", "Shimla", "Ranchi", "Bengaluru",
            "Thiruvananthapuram", "Bhopal", "Mumbai", "Imphal", "Shillong",
            "Aizawl", "Kohima", "Bhubaneswar", "Jaipur", "Gangtok", "Chennai",
            "Hyderabad", "Agartala", "Lucknow", "Dehradun", "Kolkata",
            "Port Blair", "Chandigarh", "Daman", "New Delhi", "Kavaratti", "Puducherry"
        ]

        # List to store weather data for each city
        weather_data_list = []

        for capital in indian_capitals:
           
           
            
            try:
                url = f'https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={api_key}'
                response = requests.get(url)
                
                # Check if request was successful
                if response.status_code != 200:
                    print(f"Error fetching data for {capital}: Status code {response.status_code}")
                    continue
                
                weather_data = response.json()
                
                # Extract relevant data
                flat_data = {
                    'longitude': weather_data.get('coord', {}).get('lon'),
                    'latitude': weather_data.get('coord', {}).get('lat'),
                    'weather_id': weather_data.get('weather', [{}])[0].get('id'),
                    'weather_main': weather_data.get('weather', [{}])[0].get('main'),
                    'weather_description': weather_data.get('weather', [{}])[0].get('description'),
                    'weather_icon': weather_data.get('weather', [{}])[0].get('icon'),
                    'temperature': weather_data.get('main', {}).get('temp') - 273.15,  # Convert to Celsius
                    'feels_like': weather_data.get('main', {}).get('feels_like') - 273.15,
                    'temp_min': weather_data.get('main', {}).get('temp_min') - 273.15,
                    'temp_max': weather_data.get('main', {}).get('temp_max') - 273.15,
                    'pressure': weather_data.get('main', {}).get('pressure'),
                    'humidity': weather_data.get('main', {}).get('humidity'),
                    'sea_level': weather_data.get('main', {}).get('sea_level'),
                    'ground_level': weather_data.get('main', {}).get('grnd_level'),
                    'visibility': weather_data.get('visibility'),
                    'wind_speed': weather_data.get('wind', {}).get('speed'),
                    'wind_degree': weather_data.get('wind', {}).get('deg'),
                    'wind_gust': weather_data.get('wind', {}).get('gust'),
                    'rain_1h': weather_data.get('rain', {}).get('1h'),
                    'clouds': weather_data.get('clouds', {}).get('all'),
                    'datetime': datetime.fromtimestamp(weather_data.get('dt', 0)).isoformat(),
                    'country': weather_data.get('sys', {}).get('country'),
                    'sunrise': datetime.fromtimestamp(weather_data.get('sys', {}).get('sunrise', 0)).isoformat(),
                    'sunset': datetime.fromtimestamp(weather_data.get('sys', {}).get('sunset', 0)).isoformat(),
                    'timezone': weather_data.get('timezone'),
                    'city_id': weather_data.get('id'),
                    'city_name': weather_data.get('name')
                }
                
                # Append to the list
                weather_data_list.append(flat_data)
                
                print(f"Successfully processed data for {capital}")
                
            except Exception as e:
                print(f"Error processing data for {capital}: {str(e)}")
                continue

        # Save JSON data to S3
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = "weather_data_today.json"
        print("Successfully saved data")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{file_name}",
            Body=json.dumps(weather_data_list, indent=2)  # Convert list to JSON format
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Weather data saved to S3')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
