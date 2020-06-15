import requests
from koimetrics.settings import API_HOST, API_AUTH_KEY

def get_website_key(host, end_date):
    message  = "%s/DJANGO/new_apikey?secret_key=%s&host=%s&end_date=%s"
    response = requests.get(message % (API_HOST, API_AUTH_KEY, host, end_date))
    results  = response.json()
    if results.get("statusCode") == 1:
        key = results.get("data").get("api_key")
        return key
    else:
        return results

def sessions(host, apikey, seconds = 10):
    message  = f"{API_HOST}/DJANGO/get_sessions/?secret_key={API_AUTH_KEY}&host={host}&apikey={apikey}&seconds={seconds}"
    response = requests.get(message)
    results  = response.json().get("results")
    results = results if results else list()
    return results