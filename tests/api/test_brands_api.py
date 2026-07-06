import pytest
import requests

pytestmark = pytest.mark.regression


def test_brands_list_returns_200_with_expected_schema(api_base_url):
    response = requests.get(f"{api_base_url}/api/brandsList", timeout=10)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 3

    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0
    for brand in body["brands"]:
        assert "id" in brand
        assert "brand" in brand


def test_brands_list_rejects_unsupported_http_method(api_base_url):
    response = requests.post(f"{api_base_url}/api/brandsList", timeout=10)

    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
