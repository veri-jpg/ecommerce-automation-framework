import os
import uuid

import allure
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")


@pytest.fixture(scope="session")
def base_url():
    """Overrides pytest-playwright's base_url fixture so every page/context
    is created against the URL configured in .env - switching environments
    (staging/prod) means editing one file instead of every test."""
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL


@pytest.fixture
def api_user(api_base_url):
    """Creates a real account via the public API (faster and more reliable
    than driving the signup UI) so UI tests have valid credentials to log in
    with, then deletes it via the API afterwards - keeps the shared public
    site free of leftover test accounts."""
    email = f"qa-{uuid.uuid4().hex[:10]}@example.com"
    password = "TestPass123!"
    name = "QA Data User"
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "5",
        "birth_year": "1995",
        "firstname": "QA",
        "lastname": "User",
        "company": "QA Co",
        "address1": "123 Test Street",
        "address2": "",
        "country": "India",
        "zipcode": "12345",
        "state": "Test State",
        "city": "Test City",
        "mobile_number": "08123456789",
    }
    requests.post(f"{api_base_url}/api/createAccount", data=payload, timeout=15)

    yield {"name": name, "email": email, "password": password}

    requests.delete(f"{api_base_url}/api/deleteAccount", data={"email": email, "password": password}, timeout=15)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attaches a final-state screenshot to the Allure report for every UI
    test (pass or fail). Runs as part of test-report generation, right after
    the test body returns and before any fixture teardown starts - so the
    `page` fixture (grabbed from item.funcargs) is guaranteed to still be
    open, regardless of fixture teardown order. API tests never populate a
    `page` funcarg, so nothing is launched for them."""
    outcome = yield
    result = outcome.get_result()
    setattr(item, f"rep_{result.when}", result)

    if result.when != "call":
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        screenshot = page.screenshot()
    except Exception:
        return

    name = "failure-screenshot" if result.failed else "final-state-screenshot"
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
