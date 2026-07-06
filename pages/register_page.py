import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class AccountInfoPage(BasePage):
    def expect_loaded(self):
        expect(self.page.get_by_text(re.compile("enter account information", re.I))).to_be_visible()

    def fill_account_details(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        state: str,
        city: str,
        zipcode: str,
        mobile_number: str,
        title: str = "Mr",
    ):
        gender_id = "#id_gender1" if title == "Mr" else "#id_gender2"
        self.page.locator(gender_id).check(force=True)
        self.page.locator('[data-qa="password"]').fill(password)
        self.page.locator('[data-qa="first_name"]').fill(first_name)
        self.page.locator('[data-qa="last_name"]').fill(last_name)
        self.page.locator('[data-qa="address"]').fill(address)
        self.page.locator('[data-qa="state"]').fill(state)
        self.page.locator('[data-qa="city"]').fill(city)
        self.page.locator('[data-qa="zipcode"]').fill(zipcode)
        self.page.locator('[data-qa="mobile_number"]').fill(mobile_number)

    def submit(self):
        self.page.locator('[data-qa="create-account"]').click()
        self.page.wait_for_url("**/account_created")


class AccountCreatedPage(BasePage):
    def expect_account_created(self):
        expect(self.page.get_by_text(re.compile("account created!", re.I))).to_be_visible()

    def continue_to_home(self):
        self.page.locator('[data-qa="continue-button"]').click()
        self.page.wait_for_url("https://automationexercise.com/")
