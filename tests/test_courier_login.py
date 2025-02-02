import allure
import requests
from data.endpoints import Endpoints
from data.response_texts import ResponseMessages

@allure.story('Test courier login')
class TestCourierLogin:

    @allure.title('Assert status code of successful login')
    def test_login_valid(self, create_courier):
        response = requests.post(Endpoints.COURIER_LOGIN, json={
            "login": create_courier["login"],
            "password": create_courier["password"]
        })
        assert response.status_code == 200, "Код ответа должен быть 200"
        assert "id" in response.json(), "Ответ должен содержать id"

    @allure.title('Assert error status code when fill invalid credentials')
    def test_login_invalid_credentials(self, create_courier):
        response = requests.post(Endpoints.COURIER_LOGIN, json={
            "login": create_courier["login"],
            "password": "wrong_password"
        })
        assert response.status_code == 404
        assert response.json()["message"] == ResponseMessages.ACCOUNT_NOT_FOUND

    @allure.title('Assert error status code when some fields stayed unfilled')
    def test_login_missing_fields(self):
        payload = {}
        response = requests.post(Endpoints.COURIER_LOGIN, json=payload)
        assert response.status_code == 504, f"Ожидался код 504, но пришёл {response.status_code}."
        assert ResponseMessages.SERVICE_UNAVAILABLE in response.text, (
            f"Ожидалось сообщение 'Service unavailable', но получено: {response.text}"
        )