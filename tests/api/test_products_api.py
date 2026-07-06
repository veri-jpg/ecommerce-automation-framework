import pytest
import requests

pytestmark = pytest.mark.regression


def test_products_list_returns_200_with_expected_schema(api_base_url):
    response = requests.get(f"{api_base_url}/api/productsList", timeout=10)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 3

    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0

    first_product = body["products"][0]
    for field in ("id", "name", "price", "brand", "category"):
        assert field in first_product
    assert "usertype" in first_product["category"]
    assert "category" in first_product["category"]


def test_products_list_rejects_unsupported_http_method(api_base_url):
    response = requests.post(f"{api_base_url}/api/productsList", timeout=10)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
