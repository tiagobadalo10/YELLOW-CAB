import http
import json
from locust import HttpUser, task, between

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

class QuickstartUser(HttpUser):
    wait_time = between(5, 15)

    token = get_auth_token()

    @task
    def time(self):

        PULocationName = "Central Park"
        DOLocationName = "JFK Airport"
        PULocationName2 = "Central Park"
        DOLocationName2 = "Bronx Park"
        token = self.token

        base_url = "api/stats/time"
        params = {
            "PULocationName": PULocationName,
            "DOLocationName": DOLocationName,
            "PULocationName2": PULocationName2,
            "DOLocationName2": DOLocationName2,            
            "token": token
        }

        self.client.get(base_url, params=params, verify=False)

    @task
    def congestion(self):

        PULocationName = "Central Park"
        DOLocationName = "JFK Airport"
        PULocationName2 = "Central Park"
        DOLocationName2 = "Bronx Park"
        token = self.token

        base_url = "api/stats/congestion"
        params = {
            "PULocationName": PULocationName,
            "DOLocationName": DOLocationName,
            "PULocationName2": PULocationName2,
            "DOLocationName2": DOLocationName2,            
            "token": token
        }

        self.client.get(base_url, params=params, verify=False)

    @task
    def cabs(self):

        LocationName = "Central Park"
        LocationName2 = "Bronx Park"
        token = self.token

        base_url = "api/stats/cabs"
        params = {
            "LocationName": LocationName,
            "LocationName2": LocationName2,
            "token": token
        }
        self.client.get(base_url, params=params, verify=False)
        