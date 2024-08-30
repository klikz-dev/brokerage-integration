import requests

TIINGO_API_KEY = 'c30186445fffaaa4ad55ae05e829da57a59dda94'

API_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization' : f'Token {TIINGO_API_KEY}'
}

def test_tiingo_api():
    response = requests.get("https://api.tiingo.com/api/test/", headers=API_HEADERS)
    return response.json()