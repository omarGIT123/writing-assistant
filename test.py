import requests
import json

# Define the URL of your Flask app's endpoint
url = "http://127.0.0.1:5000/suggestions"

# Prepare the data to send
data = {"text": "Once upon a time", "prompt": "Tell me a story about"}

# Send the POST request with the JSON data
response = requests.post(url, json=data)

# Print the response from the server
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
