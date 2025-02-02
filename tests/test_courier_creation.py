import allure
import pytest
import requests
from data.endpoints import Endpoints
from data.response_texts import ResponseMessages

@allure.story('Test courier creation')
class TestCourierCreation:

    @allure.title('Assert status code of successful courier creation')
    def test_create_valid_courier(self, courier_data):
        response = requests.post(Endpoints.COURIER, json=courier_data)
        assert response.status_code == 201, "Код ответа должен быть 201"
        assert response.json() == {'ok': True}, "Ответ должен содержать {'ok': true}"

    @allure.title('Assert error status code when try to create existing courier')
    def test_create_existing_courier(self, create_courier):
        response = requests.post(Endpoints.COURIER, json=create_courier)
        assert response.status_code == 409, "Код ответа должен быть 409 при создании курьера с существующим логином"
        assert response.json()["message"] == ResponseMessages.LOGIN_USED

    @allure.title('Assert status code when fields of courier creation not filled')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_fields(self, missing_field, courier_data):
        del courier_data[missing_field]
        response = requests.post(Endpoints.COURIER, json=courier_data)
        assert response.status_code == 400, f"Код ответа должен быть 400 при отсутствии поля {missing_field}"
        assert response.json()["message"] == ResponseMessages.MISSING_FIELDS, \
            f"Сообщение об ошибке должно быть корректным при отсутствии поля {missing_field}"

    @allure.title('Assert status code when only some field of courier creation not filled')
    def test_create_courier_required_fields(self):
        invalid_data = {}
        response = requests.post(Endpoints.COURIER, json=invalid_data)
        assert response.status_code == 400, "Код ответа должен быть 400 при отсутствии обязательных полей"
        assert response.json()["message"] == ResponseMessages.MISSING_FIELDS