import allure
import pytest
import requests
from data.endpoints import Endpoints
from data.test_data import ORDER_DATA

@allure.story('Test order creation')
class TestOrderCreation:

    @allure.title('Assert status code of successful order creation')
    @pytest.mark.parametrize("colors", [
        (["BLACK"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    def test_create_order(self, colors):
        order_data = ORDER_DATA.copy()
        response = requests.post(Endpoints.ORDER, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json(), "Ответ должен содержать track"