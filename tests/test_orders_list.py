import allure
import requests
from data.endpoints import Endpoints
from data.test_data import ORDER_DATA

@allure.story('Test getting order list success')
class TestOrdersList:

    @allure.title('Assert status code when getting order list ')
    def test_get_orders_list(self):
        requests.post(Endpoints.ORDER, json=ORDER_DATA)
        response = requests.get(Endpoints.ORDER)
        assert response.status_code == 200 # 504 ошибка вылетает периодически, проблемы с сервером?
        orders = response.json().get("orders")
        assert isinstance(orders, list)
        for order in orders:
            assert "id" in order