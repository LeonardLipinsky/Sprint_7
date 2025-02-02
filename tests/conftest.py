import pytest
import requests
from helpers.generator import generate_random_string
from data.endpoints import Endpoints

@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

@pytest.fixture
def create_courier(courier_data):
    response = requests.post(Endpoints.COURIER, json=courier_data)
    if response.status_code == 201:
        yield courier_data
        response = requests.post(Endpoints.COURIER_LOGIN, json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{Endpoints.COURIER}/{courier_id}")
    else:
        yield None