# Weather Data Pipeline with AWS Lambda, S3, and Power BI

This project automates the process of fetching, storing, and visualizing daily weather data from OpenWeatherMap. The goal is to create a dynamic Power BI dashboard that updates daily with fresh weather insights. 

## Overview

- **Data Source**: OpenWeatherMap API provides real-time weather data for selected locations.
- **ETL Pipeline**: AWS Lambda and S3 handle the data extraction, storage, and daily updates.
- **Visualization**: Power BI transforms and visualizes the data, providing clear insights into daily weather patterns.

## Project Workflow

### Step 1: Fetch Weather Data
An AWS Lambda function, set up in Python, is configured to fetch weather data daily at 8 AM UTC using a CloudWatch trigger. This data includes various weather metrics (e.g., temperature, humidity, wind speed) for specified cities.

### Step 2: Store Data in S3
After fetching the data, the Lambda function saves it as a JSON file in an S3 bucket. The JSON file is set to overwrite daily, so only the latest data is kept.

### Step 3: Import Data into Power BI
Power BI connects to the S3 bucket using a Python script with `boto3` (AWS SDK for Python) and secret keys. This script pulls in the latest JSON data for further processing.

### Step 4: Data Transformation
In Power BI, the data is cleaned and transformed using the Query Editor to ensure consistency and prepare it for analysis. Some of these transformations include:
- Removing any unnecessary fields.
- Formatting data types for compatibility with DAX calculations.

### Step 5: Create DAX Measures
Custom DAX measures are created to perform calculations that add deeper insights to the dashboard, such as temperature averages, peak wind speeds, or percentage changes in humidity.

### Step 6: Build Power BI Visualizations
Using Power BI’s visualization tools, a dashboard is created to display key weather insights. This can include line charts, bar graphs, and tables showing weather trends for each day.

### Step 7: Daily Data Refresh
The Lambda function’s daily trigger ensures the S3 JSON file is updated each morning. Power BI is then refreshed to pull in the latest data and update the dashboard automatically, ensuring up-to-date visualizations every day.

## Technical Details

- **Lambda Function**: Written in Python, the Lambda function makes a request to the OpenWeatherMap API, receives the data in JSON format, and saves it to an S3 bucket.
- **Power BI Import**: Power BI uses a Python script to connect to S3, fetch the JSON, and load it into Power BI.
- **DAX and Query Editor**: Transformations are done in Power BI using the Query Editor, and calculations are performed using DAX.

## Prerequisites

- AWS Account with permissions for Lambda, S3, and EventBridge (for scheduling the Lambda function).
- Power BI Desktop.
- OpenWeatherMap API Key.
- Python (for local testing of Lambda) and `boto3` library (for connecting Power BI to AWS).

## Installation and Setup

1. **Set up Lambda Function**:
   - Configure a new Lambda function in AWS.
   - Add your OpenWeatherMap API key in the environment variables.
   - Write the Python code to fetch weather data and store it in an S3 bucket.

2. **Configure CloudWatch Trigger**:
   - Set up a CloudWatch rule to trigger the Lambda function daily at 8 AM UTC.

3. **Power BI Script**:
   - In Power BI, write a Python script using `boto3` to fetch the JSON file from S3.
   - Load and transform this data in Power BI.

4. **Create Visualizations**:
   - Use Power BI’s tools to design a dashboard with the imported weather data.

