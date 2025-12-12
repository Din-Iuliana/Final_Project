import requests 
from data_cleaning import clean_1

def get_data(url):
    response = requests.get(url)
    return clean_1(response.json())