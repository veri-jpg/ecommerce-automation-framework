from playwright.sync_api import expect

from pages.base_page import BasePage


class ProductsPage(BasePage):
    def navigate(self):
        self.page.goto("/products")

    def search(self, keyword: str):
        self.page.locator("#search_product").fill(keyword)
        self.page.locator("#submit_search").click()

    def expect_search_results_visible(self):
        expect(self.page.locator(".title.text-center")).to_be_visible()
        expect(self.page.locator(".product-image-wrapper").first).to_be_visible()

    def add_product_to_cart(self, index: int = 0):
        self.page.locator(".product-image-wrapper .add-to-cart").nth(index).click()
        self.page.wait_for_selector("#cartModal", state="visible")

    def go_to_cart_from_modal(self):
        self.page.locator("#cartModal").get_by_text("View Cart").click()
        self.page.wait_for_url("**/view_cart")
