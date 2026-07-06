from pages.base_page import BasePage


class CartPage(BasePage):
    def get_item_count(self) -> int:
        return self.page.locator("#cart_info_table tbody tr").count()

    def get_item_names(self) -> list[str]:
        return self.page.locator("#cart_info_table .cart_description h4").all_inner_texts()

    def proceed_to_checkout(self):
        self.page.locator(".check_out").click()
        self.page.wait_for_url("**/checkout")
