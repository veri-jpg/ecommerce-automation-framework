import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def navigate(self):
        self.page.goto("/login")

    def login(self, email: str, password: str):
        self.page.locator('[data-qa="login-email"]').fill(email)
        self.page.locator('[data-qa="login-password"]').fill(password)
        self.page.locator('[data-qa="login-button"]').click()

    def signup(self, name: str, email: str):
        self.page.locator('[data-qa="signup-name"]').fill(name)
        self.page.locator('[data-qa="signup-email"]').fill(email)
        self.page.locator('[data-qa="signup-button"]').click()
        self.page.wait_for_url("**/signup")

    def expect_login_heading_visible(self):
        expect(self.page.get_by_role("heading", name="Login to your account")).to_be_visible()

    def expect_login_error_visible(self):
        expect(self.page.get_by_text("Your email or password is incorrect!")).to_be_visible()

    def expect_still_on_login_page(self):
        """When required/format validation blocks submission client-side,
        the browser never posts to the server, so no error text appears -
        the only observable signal is that we're still on /login."""
        expect(self.page).to_have_url(re.compile(r"/login/?$"))
        expect(self.page.get_by_text("Your email or password is incorrect!")).not_to_be_visible()
