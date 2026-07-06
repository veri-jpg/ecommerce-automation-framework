import pytest
from faker import Faker

from pages.login_page import LoginPage
from pages.register_page import AccountCreatedPage, AccountInfoPage

fake = Faker()


@pytest.mark.regression
def test_register_new_account_shows_welcome_message(page):
    name = fake.name()
    email = fake.unique.email()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.signup(name, email)

    account_info_page = AccountInfoPage(page)
    account_info_page.expect_loaded()
    account_info_page.fill_account_details(
        password="TestPass123!",
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address=fake.street_address(),
        state=fake.state(),
        city=fake.city(),
        zipcode=fake.postcode(),
        mobile_number=fake.numerify("08##########"),
    )
    account_info_page.submit()

    account_created_page = AccountCreatedPage(page)
    account_created_page.expect_account_created()
    account_created_page.continue_to_home()

    account_created_page.expect_logged_in_as(name)

    account_created_page.delete_account_and_confirm()
