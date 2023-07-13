import json
import requests

IP = "127.0.0.1"
SPACE = "%20"

def test_get_tips(token):
    PULocationName = "Chinatown"
    DOLocationName = "Central Park"

    base_url = f"http://{IP}:8082/api/bi/tips"
    params = {
        "PULocationName": PULocationName,
        "DOLocationName": DOLocationName,
        "token": token
    }
    response = requests.get(base_url, params=params, timeout=10)

    expected_output = {"avg_tips": 4.13,
                       "count_tips": 25, "max_tips": 7.65, "min_tips": 0}

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.text) == expected_output


def test_get_amounts(token):
    PULocationName = "Chinatown"
    DOLocationName = "Central Park"

    base_url = f"http://{IP}:8082/api/bi/amount"
    params = {
        "PULocationName": PULocationName,
        "DOLocationName": DOLocationName,
        "token": token
    }
    response = requests.get(base_url, params=params, timeout=10)

    expected_output = {"avg_amount": 31.19, "count_amount": 25,
                       "max_amount": 45.95, "min_amount": 23.3, "total_amount": 779.65}

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.text) == expected_output
