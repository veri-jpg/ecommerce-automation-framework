from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def add_order_comment(self, comment: str):
        self.page.locator('textarea[name="message"]').fill(comment)

    def place_order(self):
        self.page.get_by_role("link", name="Place Order").click()
        self.page.wait_for_url("**/payment")
