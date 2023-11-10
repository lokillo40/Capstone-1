import requests
from flask import flash
from config import Config

# Define a function to perform the search operation
def perform_search(search_query, API_URL, app):
    
    # Retrieve the API key from the current_app.config
    rapidapi_key = app.config.get('RAPIDAPI_KEY')
    # Define the query parameters for the API call
    querystring = {
        "limit": "10",  # Limit the number of results
        "releaseDate": "gte:2020-10-10",  # Filter based on release date can be whatever date you choose
        "name": search_query  # The search term entered by the user
    }
    # Define the headers for the API call
    headers = {
        "X-RapidAPI-Key": rapidapi_key,  # Retrieve the API key from current_app.config
        "X-RapidAPI-Host": "v1-sneakers.p.rapidapi.com"  # API host
    }
    
    try:
        # Make the GET request to the API with the headers and query parameters
        response = requests.get(API_URL, headers=headers, params=querystring)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the parsed JSON data and no error
            return response.json(), None
        else:
            # Return None for data and an error message
            return None, "Error: Unable to retrieve search results from the API"
    except requests.exceptions.RequestException as e:
        # Catch any exceptions during the API call and return None for data and the error message
        return None, f"Error: {str(e)}"

