import allure
import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@allure.title('generating courier data')
@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
@allure.title('Creating and deleting courier')
@pytest.fixture
def create_courier(courier_data):
    response = requests.post(f"{BASE_URL}/courier", json=courier_data)
    if response.status_code == 201:
        yield courier_data
        response = requests.post(f"{BASE_URL}/courier/login", json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{BASE_URL}/courier/{courier_id}")
    else:
        yield None

@allure.story('Test courier creation')
class TestCourierCreation:

    @allure.title('Assert status code of successful courier creation')
    def test_create_valid_courier(self, courier_data):
        response = requests.post(f"{BASE_URL}/courier", json=courier_data)
        assert response.status_code == 201, "Код ответа должен быть 201"
        assert response.json() == {'ok': True}, "Ответ должен содержать {'ok': true}"

    @allure.title('Assert error status code when try to create existing courier')
    def test_create_existing_courier(self, create_courier):
        response = requests.post(f"{BASE_URL}/courier", json=create_courier)
        assert response.status_code == 409, "Код ответа должен быть 409 при создании курьера с существующим логином"
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Assert status code when fields of courier creation not filled')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_fields(self, missing_field, courier_data):
        del courier_data[missing_field]
        response = requests.post(f"{BASE_URL}/courier", json=courier_data)
        assert response.status_code == 400, f"Код ответа должен быть 400 при отсутствии поля {missing_field}"
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи", \
            f"Сообщение об ошибке должно быть корректным при отсутствии поля {missing_field}"

    @allure.title('Assert status code when only some field of courier creation not filled')
    def test_create_courier_required_fields(self):
        invalid_data = {}
        response = requests.post(f"{BASE_URL}/courier", json=invalid_data)
        assert response.status_code == 400, "Код ответа должен быть 400 при отсутствии обязательных полей"
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

@allure.story('Test courier login')
class TestCourierLogin:

    @allure.title('Assert status code of successful login')
    def test_login_valid(self, create_courier):
        response = requests.post(f"{BASE_URL}/courier/login", json={
            "login": create_courier["login"],
            "password": create_courier["password"]
        })
        assert response.status_code == 200, "Код ответа должен быть 200"
        assert "id" in response.json(), "Ответ должен содержать id"

    @allure.title('Assert error status code when fill invalid credentials')
    def test_login_invalid_credentials(self, create_courier):
        response = requests.post(f"{BASE_URL}/courier/login", json={
            "login": create_courier["login"],
            "password": "wrong_password"
        })
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Assert error status code when some fields stayed unfilled')
    def test_login_missing_fields(self):
        payload = {}
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 504, f"Ожидался код 504, но пришёл {response.status_code}."
        assert "Service unavailable" in response.text, (
            f"Ожидалось сообщение 'Service unavailable', но получено: {response.text}"
        )

@allure.story('Test order creation')
class TestOrderCreation:

    @allure.title('Assert status code of successful order creation')
    @pytest.mark.parametrize("colors", [
        (["BLACK"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    def test_create_order(self, colors):
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, apt. 142",
            "metroStation": "4",
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Саске, вернись в Коноху!",
            "color": colors
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 201
        assert "track" in response.json(), "Ответ должен содержать track"

@allure.story('Test getting order list success')
class TestOrdersList:

    @allure.title('Assert status code when getting order list ')
    def test_get_orders_list(self):
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, apt. 142",
            "metroStation": "4",
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Саске, вернись в Коноху!",
            "color": "BLACK"
        }
        requests.post(f"{BASE_URL}/orders", json=order_data)
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        orders = response.json().get("orders")
        assert isinstance(orders, list)
        for order in orders:
            assert "id" in order
