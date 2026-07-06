import re

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def expect_logged_in_as(self, name: str):
        expect(self.page.get_by_text(f"Logged in as {name}")).to_be_visible()

    def delete_account_and_confirm(self):
        """Teardown helper: automationexercise.com is a shared public site, so
        tests that register an account clean up after themselves."""
        self.page.goto("/delete_account")
        expect(self.page.get_by_text(re.compile("account deleted!", re.I))).to_be_visible()
