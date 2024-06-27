import requests


def fetch_data(url, params):
    response = requests.get(url, params=params)
    return response.json()
