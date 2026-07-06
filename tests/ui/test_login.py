import json
from pathlib import Path

import pytest

from pages.login_page import LoginPage

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "login_data.json"
LOGIN_CASES = json.loads(DATA_FILE.read_text())


@pytest.mark.regression
@pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["case"] for c in LOGIN_CASES])
def test_login_rejects_invalid_data_combinations(page, case):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.expect_login_heading_visible()

    login_page.login(case["email"], case["password"])

    if case["expected_behavior"] == "server_error":
        login_page.expect_login_error_visible()
    else:
        login_page.expect_still_on_login_page()


@pytest.mark.smoke
def test_login_with_valid_and_wrong_password(page, api_user):
    """Sets up a real account via the API (createAccount), then verifies both
    the wrong-password and valid-password login paths through the UI."""
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login(api_user["email"], "TotallyWrongPassword!")
    login_page.expect_login_error_visible()

    login_page.navigate()
    login_page.login(api_user["email"], api_user["password"])
    login_page.expect_logged_in_as(api_user["name"])
