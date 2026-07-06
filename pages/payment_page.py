import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class PaymentPage(BasePage):
    def pay(self, name_on_card: str, card_number: str, cvc: str, expiry_month: str, expiry_year: str):
        self.page.locator('[data-qa="name-on-card"]').fill(name_on_card)
        self.page.locator('[data-qa="card-number"]').fill(card_number)
        self.page.locator('[data-qa="cvc"]').fill(cvc)
        self.page.locator('[data-qa="expiry-month"]').fill(expiry_month)
        self.page.locator('[data-qa="expiry-year"]').fill(expiry_year)
        self.page.locator('[data-qa="pay-button"]').click()
        self.page.wait_for_url("**/payment_done/**")

    def expect_order_confirmed(self):
        expect(self.page.get_by_text(re.compile("order placed!", re.I))).to_be_visible()
        expect(self.page.get_by_text("Congratulations! Your order has been confirmed!")).to_be_visible()
