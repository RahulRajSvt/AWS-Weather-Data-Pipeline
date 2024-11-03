# AWS-Weather-Data-Pipeline
An automated weather data pipeline fetches daily data from OpenWeatherMap via AWS Lambda, stores it as JSON in an S3 bucket, and imports it into Power BI using Boto3. Data is cleaned, transformed, and enhanced with DAX measures before visualizations are created. The pipeline refreshes each morning, providing up-to-date weather insights.
