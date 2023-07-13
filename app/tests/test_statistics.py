import json
import requests


IP = "127.0.0.1"
SPACE = "%20"


def test_get_stats_by_locations(token):
    PULocationName = "Central Park"
    DOLocationName = "JFK Airport"
    PULocationName2 = "Central Park"
    DOLocationName2 = "Bronx Park"

    base_url = f"http://{IP}:8083/api/stats/time"
    params = {
        "PULocationName": PULocationName,
        "DOLocationName": DOLocationName,
        "PULocationName2": PULocationName2,
        "DOLocationName2": DOLocationName2,
        "token": token
    }
    response = requests.get(base_url, params=params, timeout=10)

    expected_output = {
        "trip1": {
            "min_time": 0.02, "max_time": 1438.08, "avg_time": 64.76,
        },
        "trip2": {
            "min_time": 0.02, "max_time": 46.73, "avg_time": 32.11,
        }}

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.text) == expected_output


def test_get_cab_statistics(token):
    LocationName = "Central Park"
    LocationName2 = "Bronx Park"

    base_url = f"http://{IP}:8083/api/stats/cabs"
    params = {
        "LocationName": LocationName,
        "LocationName2": LocationName2,
        "token": token
    }
    response = requests.get(base_url, params=params, timeout=10)

    expected_output = {"number_cabs_first_location": 102993,
                       "number_cabs_second_location": 276}

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.text) == expected_output


def test_get_congestion_stats(token):
    PULocationName = "Central Park"
    DOLocationName = "JFK Airport"
    PULocationName2 = "Central Park"
    DOLocationName2 = "Bronx Park"

    base_url = f"http://{IP}:8083/api/stats/congestion"
    params = {
        "PULocationName": PULocationName,
        "DOLocationName": DOLocationName,
        "PULocationName2": PULocationName2,
        "DOLocationName2": DOLocationName2,
        "token": token
    }
    response = requests.get(base_url, params=params, timeout=10)

    expected_output = {
        "trip1": {
            "min_congestion": 0, "max_congestion": 2.5, "avg_congestion": 2.04,
        },
        "trip2": {
            "min_congestion": 0, "max_congestion": 2.5, "avg_congestion": 2.05,
        }}

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.text) == expected_output
