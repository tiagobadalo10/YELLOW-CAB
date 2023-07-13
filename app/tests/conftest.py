import http.client
import json
import time
import pytest

@pytest.fixture(scope="session", name="token")
def getToken():
    token = get_auth_token()
    time.sleep(1)
    return token


'''
This function mocks the authentication microservice by sending a POST request with a
JSON payload containing the user's credentials (username and password), client ID, 
client secret, audience, and grant type. The response from the server is then parsed as a JSON
object, and the access token is extracted and returned. This token can be used to authenticate
subsequent requests to the API.
'''


def get_auth_token():
    conn = http.client.HTTPSConnection("dev-yellow-cab.uk.auth0.com")

    payload = """
        {
            "username": "yellowcabtest@gmail.com",
            "password": "YellowCab2023!",
            "client_id": "8UbBpha6A8WRHqNccB9hVLLOajOE5sTN",
            "client_secret": "MGYdyvlrCSPhAY1IIqiDJn09JPplYUXH6WRj6gbHUGZmDhdkVygLwXYoOz1ci2Pu",
            "audience": "https://yellowcab.com",
            "grant_type": "password"
        }
        """

    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))["access_token"]
